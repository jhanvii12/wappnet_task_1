from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification
from .serializers import (
    NotificationCreateSerializer,
    NotificationListSerializer,
    UpdateNotificationStatusSerializer,
    DeleteNotificationSerializer
)
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  

User = get_user_model()

class NotificationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=NotificationCreateSerializer)
    def post(self, request):
        if not request.user.is_staff:  # Only admin or staff can send notifications
            return Response({"error": "Permission denied. Only admins can send notifications."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationCreateSerializer(data=request.data)
        if serializer.is_valid():
            recipients = User.objects.exclude(id=request.user.id)
            for recipient in recipients:
                Notification.objects.create(
                    title=serializer.validated_data['title'],
                    message=serializer.validated_data['message'],
                    recipient=recipient
                )
            return Response({"message": "Notifications sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('filter', openapi.IN_QUERY, description="Filter by read/unread/all", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        filter_param = request.query_params.get('filter', 'unread')
        
        if filter_param == 'unread':
            notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        elif filter_param == 'read':
            notifications = Notification.objects.filter(recipient=request.user, is_read=True)
        else:
            notifications = Notification.objects.filter(recipient=request.user)

        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateNotificationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UpdateNotificationStatusSerializer)
    def post(self, request):
        serializer = UpdateNotificationStatusSerializer(data=request.data)
        if serializer.is_valid():
            Notification.objects.filter(
                id__in=serializer.validated_data['ids'],
                recipient=request.user
            ).update(is_read=serializer.validated_data['status'])
            return Response({"message": "Notification status updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DeleteNotificationSerializer) 
    def post(self, request):
        serializer = DeleteNotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification_id = serializer.validated_data['id']
            
            # Try to find the notification by ID
            notification = Notification.objects.filter(id=notification_id, recipient=request.user).first()

            if notification:
                notification.delete()
                return Response({"message": "Notification deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NotificationDeleteView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(request_body=NotificationDeleteSerializer)
#     def delete(self, request):
#         serializer = NotificationDeleteSerializer(data=request.data)
#         if serializer.is_valid():
#             Notification.objects.filter(
#                 id__in=serializer.validated_data['ids'],
#                 recipient=request.user
#             ).delete()
#             return Response({"message": "Notifications deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)