from django.contrib import admin
from .models import AnalyticsReport, UserInsight, CategoryAnalytics


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'report_type', 'status', 'start_date', 'end_date', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['title', 'description', 'user__email']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'report_type', 'title', 'description', 'status')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Report Data', {
            'fields': ('data', 'summary'),
            'classes': ('collapse',)
        }),
        ('File', {
            'fields': ('report_file',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserInsight)
class UserInsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'insight_type', 'severity', 'is_read', 'created_at']
    list_filter = ['insight_type', 'severity', 'is_read', 'is_actionable', 'created_at']
    search_fields = ['title', 'message', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'insight_type', 'title', 'message', 'severity')
        }),
        ('Status', {
            'fields': ('is_read', 'is_actionable')
        }),
        ('Data', {
            'fields': ('data', 'recommendations'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CategoryAnalytics)
class CategoryAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'user', 'month', 'total_spent', 'transaction_count', 'month_over_month_change']
    list_filter = ['month', 'created_at']
    search_fields = ['category_name', 'user__email']
    date_hierarchy = 'month'
    ordering = ['-month', '-total_spent']
