from django.urls import path
from rest_framework.routers import DefaultRouter

from auth_api.viewsets.login import LoginView
from auth_api.viewsets.refresh import RefreshView
from auth_api.viewsets.register import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]

