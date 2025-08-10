from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'amount', 'period', 'created_at', 'updated_at']
    list_filter = ['period', 'created_at']
    search_fields = ['name', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'amount', 'period')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
