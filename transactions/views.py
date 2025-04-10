from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer, TransactionListSerializer
from .dashboard_serializers import DashboardSummarySerializer, MonthlyTransactionSerializer
from accounts.permissions import IsOwner
from .filters import TransactionFilter
from .pagination import CustomPageNumberPagination
from django.db.models import Count

class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for transaction categories
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).annotate(
        total_transactions=Count('transactions')
    )

class TransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for financial transactions with filtering and pagination
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPageNumberPagination
    filterset_class = TransactionFilter
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at', 'category__name']
    ordering = ['-date']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get summary data for the dashboard
        """
        # Get current month's data
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        # Calculate total income and expenses
        transactions = Transaction.objects.filter(user=request.user)
        total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance = total_income - total_expenses
        
        # Get expense breakdown by category
        expense_by_category = {}
        expense_categories = transactions.filter(transaction_type='expense').values('category__name').annotate(total=Sum('amount'))
        for item in expense_categories:
            if item['category__name']:
                expense_by_category[item['category__name']] = item['total']
        
        # Get income breakdown by category
        income_by_category = {}
        income_categories = transactions.filter(transaction_type='income').values('category__name').annotate(total=Sum('amount'))
        for item in income_categories:
            if item['category__name']:
                income_by_category[item['category__name']] = item['total']
        
        # Get monthly summary for the last 6 months
        monthly_summary = []
        for i in range(5, -1, -1):
            month = (current_month - i) % 12
            if month == 0:
                month = 12
            year = current_year
            if current_month - i <= 0:
                year -= 1
            
            month_income = transactions.filter(
                transaction_type='income',
                date__month=month,
                date__year=year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            month_expenses = transactions.filter(
                transaction_type='expense',
                date__month=month,
                date__year=year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            monthly_summary.append({
                'month': month,
                'year': year,
                'income': month_income,
                'expenses': month_expenses,
                'net': month_income - month_expenses
            })
        
        # Get recent transactions
        recent_transactions = TransactionListSerializer(
            transactions.order_by('-date')[:5],
            many=True
        ).data
        
        # Prepare dashboard data
        dashboard_data = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'expense_by_category': expense_by_category,
            'income_by_category': income_by_category,
            'monthly_summary': monthly_summary,
            'recent_transactions': recent_transactions,
            'budget_status': []  # Will be populated by budget views
        }
        
        return Response(dashboard_data)
    
    @action(detail=False, methods=['get'])
    def filter_by_date_range(self, request):
        """
        Filter transactions by date range
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {"error": "Both start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transactions = self.get_queryset().filter(date__range=[start_date, end_date])
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)