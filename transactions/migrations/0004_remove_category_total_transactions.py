# Generated by Django 5.2 on 2025-04-10 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_category_total_transactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='total_transactions',
        ),
    ]
