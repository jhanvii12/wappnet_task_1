from django.db import models

# Create your models here.
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateField()
    estimated_completion_time = models.DurationField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return self.title

