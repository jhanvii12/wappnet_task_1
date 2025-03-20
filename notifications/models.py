from django.db import models

# Create your models here.
from authentication.models import User  # Import the User model from authentication app

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Track if notification is read
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)  # Each notification is for one user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} to {self.recipient.email}"

