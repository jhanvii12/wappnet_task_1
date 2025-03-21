from django.urls import path
from .views import TaskCreateView, TaskListView, TaskDeleteView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('list/', TaskListView.as_view(), name='list_task'),
    path('delete/<int:pk>', TaskDeleteView.as_view(), name='delete_task'),
]
