from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, 
    NotificationCreateSerializer,
    NotificationPreferenceSerializer,
    NotificationMarkReadSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['notification_type', 'status', 'priority']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter notifications for the current user"""
        return Notification.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark multiple notifications as read"""
        serializer = NotificationMarkReadSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            notifications = serializer.save()
            return Response({
                'message': f'{notifications.count()} notifications marked as read',
                'count': notifications.count()
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all unread notifications as read"""
        unread_notifications = self.get_queryset().filter(status='unread')
        count = unread_notifications.update(status='read')
        return Response({
            'message': f'{count} notifications marked as read',
            'count': count
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(status='unread').count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent notifications (last 7 days)"""
        from datetime import datetime, timedelta
        recent_date = datetime.now() - timedelta(days=7)
        notifications = self.get_queryset().filter(
            created_at__gte=recent_date
        ).order_by('-created_at')[:20]
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notification preferences
    """
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter preferences for the current user"""
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the preference is created for the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        """Get current user's notification preferences"""
        try:
            preferences = NotificationPreference.objects.get(user=request.user)
            serializer = self.get_serializer(preferences)
            return Response(serializer.data)
        except NotificationPreference.DoesNotExist:
            # Create default preferences if they don't exist
            preferences = NotificationPreference.objects.create(user=request.user)
            serializer = self.get_serializer(preferences)
            return Response(serializer.data)
