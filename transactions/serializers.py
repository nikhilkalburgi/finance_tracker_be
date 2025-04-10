from rest_framework import serializers
from .models import Category, Transaction

class CategorySerializer(serializers.ModelSerializer):
    total_transactions = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'total_transactions']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # Assign the current user to the category
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'description', 'category', 'category_name',
            'transaction_type', 'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Assign the current user to the transaction
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'description', 'category', 'category_name',
            'transaction_type', 'date'
        ]
        read_only_fields = ['id']