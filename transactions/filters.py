import django_filters
from django.db.models import Q
from .models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category"
    )
    transaction_type = django_filters.ChoiceFilter(choices=Transaction.TRANSACTION_TYPES)
    
    # Custom filter for searching across multiple fields
    search = django_filters.CharFilter(method='filter_search')
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(description__icontains=value) | 
            Q(category__name__icontains=value)
        )
    
    class Meta:
        model = Transaction
        fields = ['category', 'transaction_type', 'date', 'min_amount', 'max_amount', 
                 'start_date', 'end_date', 'search']