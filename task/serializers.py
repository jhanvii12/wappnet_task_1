from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_users', 'priority', 'due_date', 'estimated_completion_time', 'status', 'created_by']
        read_only_fields = ['created_by']
