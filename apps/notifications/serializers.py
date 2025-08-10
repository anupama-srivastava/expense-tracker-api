from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_email', 'notification_type', 'title', 
            'message', 'priority', 'status', 'action_url', 'created_at', 
            'read_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'user', 'notification_type', 'title', 'message', 
            'priority', 'action_url'
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = NotificationPreference
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationMarkReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    
    def validate_notification_ids(self, value):
        from .models import Notification
        user = self.context['request'].user
        notifications = Notification.objects.filter(
            id__in=value, 
            user=user
        )
        if notifications.count() != len(value):
            raise serializers.ValidationError("Some notifications not found")
        return value
    
    def save(self):
        from .models import Notification
        user = self.context['request'].user
        notifications = Notification.objects.filter(
            id__in=self.validated_data['notification_ids'],
            user=user
        )
        notifications.update(status='read')
        return notifications
