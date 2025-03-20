# notifications/urls.py
from django.urls import path
from .views import NotificationCreateView, NotificationListView, UpdateNotificationStatusView, ListUserNotificationsView, DeleteNotificationsView

urlpatterns = [
    path('create/', NotificationCreateView.as_view(), name='create-notification'),
    path('list/', NotificationListView.as_view(), name='list-notifications'),
    path('update-status/', UpdateNotificationStatusView.as_view(), name='update-notification-status'),
    path('list-all/', ListUserNotificationsView.as_view(), name='list-all-notifications'),
    path('delete/', DeleteNotificationsView.as_view(), name='delete-notifications'),
]