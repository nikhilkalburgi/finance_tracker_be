from rest_framework import serializers
from .models import Budget
from transactions.models import Category
from transactions.serializers import CategorySerializer

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'amount', 'month', 'year']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # Assign the current user to the budget
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BudgetSummarySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    percentage_used = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Budget
        fields = [
            'id', 'category', 'category_name', 'amount', 
            'month', 'year', 'spent', 'remaining', 'percentage_used'
        ]
        read_only_fields = ['id', 'spent', 'remaining', 'percentage_used']