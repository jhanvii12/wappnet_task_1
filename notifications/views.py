from django.shortcuts import render

# Create your views here.
# notifications/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification
from .serializers import NotificationSerializer, UpdateNotificationStatusSerializer

User = get_user_model()

class NotificationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:  # Only admin or staff can send notifications
            return Response({"error": "Permission denied. Only admins can send notifications."},
                            status=status.HTTP_403_FORBIDDEN)

        # Send notification to all users except the admin
        recipients = User.objects.exclude(id=request.user.id)
        notifications = []

        for recipient in recipients:
            notification = Notification(
                title=request.data.get('title'),
                message=request.data.get('message'),
                recipient=recipient
            )
            notification.save()
            notifications.append(notification)

        return Response({"message": "Notifications sent successfully"}, status=status.HTTP_201_CREATED)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get unread notifications for the authenticated user
        notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class UpdateNotificationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateNotificationStatusSerializer(data=request.data)
        if serializer.is_valid():
            Notification.objects.filter(
                id__in=serializer.validated_data['ids'],
                recipient=request.user
            ).update(is_read=serializer.validated_data['status'])
            return Response({"message": "Notification status updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUserNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all notifications (read and unread) for the logged-in user
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')

        # Serialize the notifications
        serialized_notifications = [
            {
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'is_read': notification.is_read,
                'created_at': notification.created_at
            } for notification in notifications
        ]

        return Response(serialized_notifications, status=status.HTTP_200_OK)


class DeleteNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notification_id = request.data.get('id')
        
        if not notification_id:
            return Response({"error": "Notification ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the notification by ID
        notification = Notification.objects.filter(id=notification_id, recipient=request.user).first()

        if notification:
            notification.delete()
            return Response({"message": "Notification deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
