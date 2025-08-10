from django.contrib import admin
from .models import Category, Expense, RecurringExpense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['color', 'is_active']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'category', 'amount', 'date', 'expense_type', 'is_recurring']
    list_filter = ['expense_type', 'category', 'date', 'is_recurring']
    search_fields = ['description', 'user__email']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'category', 'amount', 'frequency', 'next_occurrence', 'is_active']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['description', 'user__email']
    ordering = ['-created_at']
