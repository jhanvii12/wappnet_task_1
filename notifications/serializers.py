from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    message = serializers.CharField(max_length=1024, required=True)

class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'recipient', 'created_at', 'updated_at']

class UpdateNotificationStatusSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    status = serializers.BooleanField(required=True)  # To mark as read or unread

class DeleteNotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    
# class NotificationDeleteSerializer(serializers.Serializer):
#     ids = serializers.ListField(child=serializers.IntegerField(), required=True)  # List of notification IDs to delete