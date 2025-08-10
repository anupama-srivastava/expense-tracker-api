from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'avatar', 'currency', 'timezone', 'is_verified')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'monthly_income', 'savings_goal', 'created_at']
    search_fields = ['user__email', 'user__username']
    list_filter = ['created_at']
