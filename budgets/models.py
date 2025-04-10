from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    
    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"
    
    class Meta:
        unique_together = ('user', 'category', 'month', 'year')