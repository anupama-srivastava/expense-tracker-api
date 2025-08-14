import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import CategoryAnalytics, UserInsight

User = get_user_model()


class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time dashboard updates
    """
    
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"dashboard_{self.user.id}"
        
        # Join user-specific group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial data
        await self.send_initial_data()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'ping':
            await self.send(text_data=json.dumps({
                'type': 'pong',
                'timestamp': timezone.now().isoformat()
            }))
        elif message_type == 'request_update':
            await self.send_dashboard_update()

    async def send_initial_data(self):
        """Send initial dashboard data"""
        data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': data
        }))

    async def send_dashboard_update(self):
        """Send dashboard update"""
        data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': data
        }))

    @database_sync_to_async
    def get_dashboard_data(self):
        """Get current dashboard data"""
        user = self.user
        
        # Get current month data
        current_month = timezone.now().replace(day=1)
        monthly_expenses = CategoryAnalytics.objects.filter(
            user=user,
            month=current_month
        ).aggregate(total=Sum('total_spent'))['total'] or 0
        
        # Get category breakdown
        category_breakdown = list(CategoryAnalytics.objects.filter(
            user=user,
            month=current_month
        ).values('category_name').annotate(
            total=Sum('total_spent'),
            count=Count('id')
        ).order_by('-total'))
        
        # Get unread insights count
        unread_insights = UserInsight.objects.filter(
            user=user,
            is_read=False
        ).count()
        
        return {
            'monthly_expenses': float(monthly_expenses),
            'category_breakdown': category_breakdown,
            'unread_insights': unread_insights,
            'last_updated': timezone.now().isoformat()
        }

    async def dashboard_update(self, event):
        """Handle dashboard updates from other parts of the system"""
        await self.send(text_data=json.dumps({
            'type': 'real_time_update',
            'data': event['data']
        }))


class ChartDataConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time chart updates
    """
    
    async def connect(self):
        self.user = self.scope["user"]
        self.chart_type = self.scope['url_route']['kwargs']['chart_type']
        self.group_name = f"chart_{self.user.id}_{self.chart_type}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial chart data
        await self.send_chart_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if text_data_json.get('type') == 'refresh':
            await self.send_chart_data()

    async def send_chart_data(self):
        """Send current chart data"""
        data = await self.get_chart_data()
        await self.send(text_data=json.dumps({
            'type': 'chart_data',
            'chart_type': self.chart_type,
            'data': data
        }))

    @database_sync_to_async
    def get_chart_data(self):
        """Get chart data based on chart type"""
        user = self.user
        
        if self.chart_type == 'expense_trend':
            return self._get_expense_trend_data(user)
        elif self.chart_type == 'category_breakdown':
            return self._get_category_breakdown_data(user)
        elif self.chart_type == 'monthly_comparison':
            return self._get_monthly_comparison_data(user)
        
        return {'error': 'Invalid chart type'}

    def _get_expense_trend_data(self, user):
        """Get expense trend data"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=365)
        
        trend_data = CategoryAnalytics.objects.filter(
            user=user,
            month__range=[start_date, end_date]
        ).values('month').annotate(
            total=Sum('total_spent')
        ).order_by('month')
        
        return {
            'labels': [item['month'].strftime('%Y-%m') for item in trend_data],
            'datasets': [{
                'label': 'Monthly Expenses',
                'data': [float(item['total']) for item in trend_data],
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            }]
        }

    def _get_category_breakdown_data(self, user):
        """Get category breakdown data"""
        category_data = CategoryAnalytics.objects.filter(
            user=user,
            month__year=timezone.now().year
        ).values('category_name').annotate(
            total=Sum('total_spent')
        ).order_by('-total')
        
        return {
            'labels': [item['category_name'] for item in category_data],
            'datasets': [{
                'data': [float(item['total']) for item in category_data],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                ]
            }]
        }

    def _get_monthly_comparison_data(self, user):
        """Get monthly comparison data"""
        current_year = timezone.now().year
        previous_year = current_year - 1
        
        current_data = CategoryAnalytics.objects.filter(
            user=user,
            month__year=current_year
        ).values('month').annotate(
            total=Sum('total_spent')
        )
        
        previous_data = CategoryAnalytics.objects.filter(
            user=user,
            month__year=previous_year
        ).values('month').annotate(
            total=Sum('total_spent')
        )
        
        return {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'datasets': [
                {
                    'label': str(current_year),
                    'data': [float(next((item['total'] for item in current_data 
                                       if item['month'].month == i), 0)) 
                            for i in range(1, 13)],
                    'borderColor': 'rgb(75, 192, 192)',
                },
                {
                    'label': str(previous_year),
                    'data': [float(next((item['total'] for item in previous_data 
                                       if item['month'].month == i), 0)) 
                            for i in range(1, 13)],
                    'borderColor': 'rgb(255, 99, 132)',
                }
            ]
        }

    async def chart_update(self, event):
        """Handle chart updates"""
        await self.send(text_data=json.dumps({
            'type': 'chart_update',
            'data': event['data']
        }))


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    """
    
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"notifications_{self.user.id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial notifications
        await self.send_initial_notifications()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if text_data_json.get('type') == 'mark_read':
            notification_id = text_data_json.get('notification_id')
            await self.mark_notification_read(notification_id)

    @database_sync_to_async
    def send_initial_notifications(self):
        """Send initial notifications"""
        notifications = UserInsight.objects.filter(
            user=self.user,
            is_read=False
        ).order_by('-created_at')[:10]
        
        notification_data = []
        for notification in notifications:
            notification_data.append({
                'id': notification.id,
                'type': notification.insight_type,
                'title': notification.title,
                'message': notification.message,
                'severity': notification.severity,
                'created_at': notification.created_at.isoformat(),
                'is_read': notification.is_read
            })
        
        self.send(text_data=json.dumps({
            'type': 'initial_notifications',
            'notifications': notification_data
        }))

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        UserInsight.objects.filter(
            id=notification_id,
            user=self.user
        ).update(is_read=True)

    async def new_notification(self, event):
        """Handle new notifications"""
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': event['notification']
        }))
