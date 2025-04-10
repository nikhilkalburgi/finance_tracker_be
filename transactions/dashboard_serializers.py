from rest_framework import serializers

class DashboardSummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense_by_category = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    income_by_category = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    monthly_summary = serializers.ListField(child=serializers.DictField())
    recent_transactions = serializers.ListField(child=serializers.DictField())
    budget_status = serializers.ListField(child=serializers.DictField())

class MonthlyTransactionSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=10, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    net = serializers.DecimalField(max_digits=10, decimal_places=2)