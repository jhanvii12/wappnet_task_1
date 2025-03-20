from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'recipient', 'created_at', 'updated_at']

class UpdateNotificationStatusSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    status = serializers.BooleanField(required=True)  # To mark as read or unread
