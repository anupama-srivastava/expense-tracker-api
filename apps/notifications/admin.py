from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'status', 'priority', 'created_at']
    list_filter = ['notification_type', 'status', 'priority', 'created_at']
    search_fields = ['title', 'message', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'title', 'message')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'read_at')
        }),
        ('Related Object', {
            'fields': ('content_type', 'object_id', 'action_url'),
            'classes': ('collapse',)
        }),
        ('Email Status', {
            'fields': ('is_email_sent', 'email_sent_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Preferences', {
            'fields': (
                'email_expense_created',
                'email_expense_updated',
                'email_budget_limit',
                'email_recurring_due',
                'email_weekly_summary',
                'email_monthly_report',
            )
        }),
        ('Push Notification Preferences', {
            'fields': (
                'push_expense_created',
                'push_budget_exceeded',
                'push_goal_achieved',
            )
        }),
        ('In-App Preferences', {
            'fields': ('in_app_all',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
