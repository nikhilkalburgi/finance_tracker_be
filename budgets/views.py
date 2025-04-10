from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When, Value
from django.utils import timezone
from .models import Budget
from .serializers import BudgetSerializer, BudgetSummarySerializer
from transactions.models import Transaction
from accounts.permissions import IsOwner

class BudgetViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for budget management
    """
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """
        Overriding the GET /budgets endpoint to include spending summaries.
        """
        queryset = self.filter_queryset(self.get_queryset())
        budget_data = []
        
        for budget in queryset:
            # Calculate total spent for this budget based on its month and year
            spent = Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                date__month=budget.month,
                date__year=budget.year
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            remaining = budget.amount - spent
            percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
            
            # Serialize the budget object using BudgetSerializer
            serialized_budget = self.get_serializer(budget).data
            
            # Add our extra calculated fields
            serialized_budget.update({
                'spent': spent,
                'remaining': remaining,
                'percentage_used': percentage_used
            })
            budget_data.append(serialized_budget)
        
        return Response(budget_data)
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """
        Get the current month's budget with spending information
        """
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        # Get all budgets for the current month
        budgets = self.get_queryset().filter(month=current_month, year=current_year)
        
        # Calculate spending for each budget category
        budget_data = []
        for budget in budgets:
            # Get total expenses for this category in the current month
            spent = Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                date__month=current_month,
                date__year=current_year
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            # Calculate remaining budget and percentage used
            remaining = budget.amount - spent
            percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
            
            budget_data.append({
                'id': budget.id,
                'category': budget.category.id,
                'category_name': budget.category.name,
                'amount': budget.amount,
                'month': budget.month,
                'year': budget.year,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': percentage_used
            })
        
        return Response(budget_data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get a summary of all budget categories with spending information
        """
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not month or not year:
            today = timezone.now().date()
            month = today.month
            year = today.year
        else:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return Response(
                    {"error": "Invalid month or year format"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get all budgets for the specified month
        budgets = self.get_queryset().filter(month=month, year=year)
        
        # Calculate spending for each budget category
        budget_summary = []
        for budget in budgets:
            # Get total expenses for this category in the specified month
            spent = Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                date__month=month,
                date__year=year
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            # Calculate remaining budget and percentage used
            remaining = budget.amount - spent
            percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
            
            budget_summary.append({
                'id': budget.id,
                'category': budget.category.id,
                'category_name': budget.category.name,
                'amount': budget.amount,
                'month': budget.month,
                'year': budget.year,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': percentage_used
            })
        
        return Response(budget_summary)