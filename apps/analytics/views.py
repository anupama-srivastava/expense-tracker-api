from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from .models import AnalyticsReport, UserInsight, CategoryAnalytics
from .serializers import (
    AnalyticsReportSerializer, AnalyticsReportCreateSerializer,
    UserInsightSerializer, UserInsightCreateSerializer,
    CategoryAnalyticsSerializer, CategoryAnalyticsCreateSerializer,
    DashboardDataSerializer, ChartDataSerializer, RealTimeUpdateSerializer,
    VoiceReportRequestSerializer, VoiceReportResponseSerializer,
    ARVisualizationDataSerializer, SmartNotificationSerializer
)

User = get_user_model()


class AnalyticsReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing analytics reports
    """
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'report_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return AnalyticsReportCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def dashboard(self, request):
        """Get comprehensive dashboard data with real-time metrics"""
        user = request.user
        
        # Calculate date ranges
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)
        
        # Get expense data
        monthly_expenses = CategoryAnalytics.objects.filter(
            user=user,
            month__gte=start_of_month
        ).aggregate(total=Sum('total_spent'))['total'] or 0
        
        yearly_expenses = CategoryAnalytics.objects.filter(
            user=user,
            month__gte=start_of_year
        ).aggregate(total=Sum('total_spent'))['total'] or 0
        
        # Get category breakdown
        category_data = CategoryAnalytics.objects.filter(
            user=user,
            month__gte=start_of_month
        ).values('category_name').annotate(
            total=Sum('total_spent'),
            count=Count('id')
        ).order_by('-total')[:10]
        
        # Get monthly trend
        monthly_trend = CategoryAnalytics.objects.filter(
            user=user,
            month__gte=start_of_year
        ).values('month').annotate(
            total=Sum('total_spent')
        ).order_by('month')
        
        # Calculate insights
        top_category = category_data[0] if category_data else None
        budget_utilization = 75.5  # Placeholder - integrate with budgets app
        savings_rate = 15.2  # Placeholder - calculate actual savings rate
        
        dashboard_data = {
            'total_expenses': yearly_expenses,
            'monthly_expenses': monthly_expenses,
            'daily_average': yearly_expenses / 365 if yearly_expenses else 0,
            'top_category': top_category['category_name'] if top_category else None,
            'budget_utilization': budget_utilization,
            'savings_rate': savings_rate,
            'expense_trend': list(monthly_trend),
            'category_breakdown': list(category_data),
            'recent_insights': UserInsightSerializer(
                UserInsight.objects.filter(user=user)[:5],
                many=True
            ).data,
            'last_updated': timezone.now()
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def charts(self, request):
        """Get chart data for various visualization types"""
        user = request.user
        chart_type = request.query_params.get('type', 'expense_trend')
        
        if chart_type == 'expense_trend':
            data = self._get_expense_trend_data(user)
        elif chart_type == 'category_breakdown':
            data = self._get_category_breakdown_data(user)
        elif chart_type == 'monthly_comparison':
            data = self._get_monthly_comparison_data(user)
        elif chart_type == 'budget_vs_actual':
            data = self._get_budget_vs_actual_data(user)
        else:
            data = {'error': 'Invalid chart type'}
        
        return Response(data, status=status.HTTP_200_OK)

    def _get_expense_trend_data(self, user):
        """Get expense trend data for charts"""
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
        """Get category breakdown data for pie charts"""
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

    def _get_budget_vs_actual_data(self, user):
        """Get budget vs actual spending data"""
        # Placeholder - integrate with budgets app
        return {
            'labels': ['Housing', 'Food', 'Transport', 'Entertainment', 'Other'],
            'datasets': [
                {
                    'label': 'Budget',
                    'data': [1000, 500, 300, 200, 400],
                    'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                },
                {
                    'label': 'Actual',
                    'data': [950, 600, 250, 300, 350],
                    'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                }
            ]
        }

    @action(detail=False, methods=['post'])
    def voice_report(self, request):
        """Generate voice-activated reports"""
        serializer = VoiceReportRequestSerializer(data=request.data)
        if serializer.is_valid():
            report_type = serializer.validated_data['report_type']
            date_range = serializer.validated_data.get('date_range', {})
            format_type = serializer.validated_data['format']
            
            # Generate report data
            report_data = self._generate_voice_report(user=request.user, 
                                                    report_type=report_type,
                                                    date_range=date_range)
            
            response_data = {
                'report_id': f"voice_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}",
                'audio_url': report_data.get('audio_url', ''),
                'transcript': report_data.get('transcript', ''),
                'summary': report_data.get('summary', ''),
                'visual_data': report_data.get('visual_data', {})
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_voice_report(self, user, report_type, date_range):
        """Generate voice report data"""
        # Placeholder implementation
        return {
            'audio_url': 'https://example.com/reports/voice_report.mp3',
            'transcript': f'Your {report_type} report is ready.',
            'summary': f'Summary of your {report_type} for the selected period.',
            'visual_data': {'chart_url': 'https://example.com/charts/report.png'}
        }

    @action(detail=False, methods=['post'])
    def ar_visualization(self, request):
        """Get AR visualization data for 3D expense visualization"""
        serializer = ARVisualizationDataSerializer(data=request.data)
        if serializer.is_valid():
            scene_type = request.data.get('scene_type', 'expense_3d')
            
            ar_data = self._generate_ar_scene(user=request.user, scene_type=scene_type)
            
            return Response(ar_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_ar_scene(self, user, scene_type):
        """Generate AR scene data"""
        # Get user's expense data
        expenses = CategoryAnalytics.objects.filter(
            user=user,
            month__year=timezone.now().year
        )
        
        objects = []
        for expense in expenses:
            objects.append({
                'id': f"expense_{expense.id}",
                'type': 'bar',
                'position': {
                    'x': len(objects) * 2,
                    'y': 0,
                    'z': 0
                },
                'scale': {
                    'x': 1,
                    'y': float(expense.total_spent) / 100,  # Scale down for visualization
                    'z': 1
                },
                'color': f"#{hash(expense.category_name) % 0xFFFFFF:06x}",
                'label': expense.category_name,
                'value': float(expense.total_spent)
            })
        
        return {
            'scene_id': f"ar_scene_{user.id}_{scene_type}",
            'objects': objects,
            'interactions': [
                {
                    'type': 'tap',
                    'target': 'bar',
                    'action': 'show_details'
                },
                {
                    'type': 'pinch',
                    'target': 'scene',
                    'action': 'zoom'
                }
            ],
            'metadata': {
                'user_id': user.id,
                'scene_type': scene_type,
                'generated_at': timezone.now().isoformat()
            }
        }

    @action(detail=False, methods=['get'])
    def smart_notifications(self, request):
        """Get context-aware smart notifications"""
        user = request.user
        
        notifications = []
        
        # Check for budget alerts
        budget_utilization = 85  # Placeholder
        if budget_utilization > 80:
            notifications.append({
                'notification_type': 'budget_warning',
                'title': 'Budget Alert',
                'message': f'You have used {budget_utilization}% of your monthly budget.',
                'priority': 'high',
                'actions': [
                    {'type': 'view_details', 'label': 'View Details'},
                    {'type': 'adjust_budget', 'label': 'Adjust Budget'}
                ],
                'context': {'utilization': budget_utilization}
            })
        
        # Check for unusual spending
        unusual_spending = True  # Placeholder logic
        if unusual_spending:
            notifications.append({
                'notification_type': 'anomaly_detection',
                'title': 'Unusual Spending Detected',
                'message': 'We noticed unusual spending in your Entertainment category.',
                'priority': 'medium',
                'actions': [
                    {'type': 'review_transactions', 'label': 'Review Transactions'}
                ]
            })
        
        return Response(notifications, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def real_time_updates(self, request):
        """Get real-time updates for dashboard"""
        user = request.user
        
        # Get latest data
        latest_expense = CategoryAnalytics.objects.filter(
            user=user
        ).order_by('-updated_at').first()
        
        updates = {
            'type': 'dashboard_update',
            'data': {
                'latest_expense': {
                    'category': latest_expense.category_name if latest_expense else None,
                    'amount': float(latest_expense.total_spent) if latest_expense else 0,
                    'timestamp': latest_expense.updated_at if latest_expense else None
                },
                'total_monthly': CategoryAnalytics.objects.filter(
                    user=user,
                    month__year=timezone.now().year,
                    month__month=timezone.now().month
                ).aggregate(total=Sum('total_spent'))['total'] or 0
            },
            'timestamp': timezone.now()
        }
        
        return Response(updates, status=status.HTTP_200_OK)


class UserInsightViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user insights
    """
    queryset = UserInsight.objects.all()
    serializer_class = UserInsightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'insight_type', 'severity', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'updated_at', 'severity']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserInsightCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all insights as read"""
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'updated_count': updated}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread insights"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)


class CategoryAnalyticsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing category analytics
    """
    queryset = CategoryAnalytics.objects.all()
    serializer_class = CategoryAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'category_name', 'month']
    search_fields = ['category_name']
    ordering_fields = ['month', 'total_spent', 'transaction_count']
    ordering = ['-month', '-total_spent']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryAnalyticsCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get category summary for current month"""
        user = request.user
        current_month = timezone.now().replace(day=1)
        
        summary = CategoryAnalytics.objects.filter(
            user=user,
            month=current_month
        ).values('category_name').annotate(
            total_spent=Sum('total_spent'),
            transaction_count=Count('id'),
            average_transaction=Avg('average_transaction')
        ).order_by('-total_spent')
        
        return Response(list(summary), status=status.HTTP_200_OK)


class InteractiveDashboardView(APIView):
    """
    API View for interactive dashboard features
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get interactive dashboard data"""
        user = request.user
        
        # Get customizable dashboard widgets
        widgets = {
            'expense_trend': self._get_expense_trend_widget(user),
            'category_pie': self._get_category_pie_widget(user),
            'budget_progress': self._get_budget_progress_widget(user),
            'savings_goal': self._get_savings_goal_widget(user),
            'recent_activity': self._get_recent_activity_widget(user),
            'upcoming_bills': self._get_upcoming_bills_widget(user)
        }
        
        return Response(widgets, status=status.HTTP_200_OK)

    def _get_expense_trend_widget(self, user):
        """Get expense trend widget data"""
        # Implementation for expense trend
        return {'type': 'line_chart', 'data': {}}

    def _get_category_pie_widget(self, user):
        """Get category pie widget data"""
        # Implementation for category pie
        return {'type': 'pie_chart', 'data': {}}

    def _get_budget_progress_widget(self, user):
        """Get budget progress widget data"""
        # Implementation for budget progress
        return {'type': 'progress_bar', 'data': {}}

    def _get_savings_goal_widget(self, user):
        """Get savings goal widget data"""
        # Implementation for savings goal
        return {'type': 'goal_tracker', 'data': {}}

    def _get_recent_activity_widget(self, user):
        """Get recent activity widget data"""
        # Implementation for recent activity
        return {'type': 'activity_feed', 'data': {}}

    def _get_upcoming_bills_widget(self, user):
        """Get upcoming bills widget data"""
        # Implementation for upcoming bills
        return {'type': 'bill_reminder', 'data': {}}
