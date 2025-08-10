from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('expense_created', 'Expense Created'),
        ('expense_updated', 'Expense Updated'),
        ('expense_deleted', 'Expense Deleted'),
        ('budget_limit', 'Budget Limit Reached'),
        ('budget_exceeded', 'Budget Exceeded'),
        ('recurring_due', 'Recurring Expense Due'),
        ('payment_reminder', 'Payment Reminder'),
        ('goal_achieved', 'Goal Achieved'),
        ('report_ready', 'Report Ready'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    
    # Generic foreign key to link to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional metadata
    action_url = models.URLField(blank=True, null=True)
    is_email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'notification_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        if self.status == 'unread':
            self.status = 'read'
            self.read_at = models.DateTimeField(auto_now=True)
            self.save()


class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_expense_created = models.BooleanField(default=True)
    email_expense_updated = models.BooleanField(default=False)
    email_budget_limit = models.BooleanField(default=True)
    email_recurring_due = models.BooleanField(default=True)
    email_weekly_summary = models.BooleanField(default=True)
    email_monthly_report = models.BooleanField(default=True)
    
    # Push notification preferences
    push_expense_created = models.BooleanField(default=True)
    push_budget_exceeded = models.BooleanField(default=True)
    push_goal_achieved = models.BooleanField(default=True)
    
    # In-app preferences
    in_app_all = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"{self.user.email} Preferences"
