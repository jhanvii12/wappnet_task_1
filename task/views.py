from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Task
from rest_framework.permissions import IsAdminUser
from .serializers import TaskSerializer
from notifications.models import Notification 
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  

User = get_user_model()

class IsAdminUserCustom(IsAuthenticated):
     # Using Django's built-in IsAdminUser permission to allow only staff members to create tasks
    permission_classes = [IsAdminUser]

class TaskCreateView(APIView):
    permission_classes = [IsAdminUserCustom]

    @swagger_auto_schema(
        operation_description="Create a new task and assign it to multiple users.",
        request_body=TaskSerializer,
        responses={
            status.HTTP_201_CREATED: "Task created successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid input"
        }
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(created_by=request.user)

            # Generate notifications for assigned users
            assigned_users = serializer.validated_data['assigned_users']
            for user in assigned_users:
                Notification.objects.create(
                    recipient=user,
                    title=f"New Task Assigned: {task.title}",
                    message=f"Task Details:\n"
                            f"Title: {task.title}\n"
                            f"Description: {task.description}\n"
                            f"Priority: {task.priority}\n"
                            f"Due Date: {task.due_date}\n"
                            f"Estimated Completion Time: {task.estimated_completion_time}\n",
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all tasks.",
        responses={
            status.HTTP_200_OK: TaskSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: "Invalid input"
        }
    )
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# delete task view

class TaskDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Delete a task by ID.",
        responses={
            status.HTTP_204_NO_CONTENT: "Task deleted successfully",
            status.HTTP_404_NOT_FOUND: "Task not found"
        }
    )
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
