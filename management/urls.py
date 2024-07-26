"""
URL configuration for project_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
     # User sign-up endpoint
    path('SignUp/',UserSignUp.as_view(),name='signup'),
     # User login endpoint
    path('login/',LoginView.as_view(),name='login'),
    # Endpoint for listing and creating projects
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    # Endpoint for retrieving, updating, and deleting a specific project by its ID
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    # Endpoint for listing and creating task
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    # Endpoint for retrieving, updating, and deleting a specific task by its ID
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    # Endpoint for listing and creating milestones
    path('milestones/', MilestoneListCreateAPIView.as_view(), name='milestone-list-create'),
    # Endpoint for retrieving, updating, and deleting a specific milestone by its ID
    path('milestones/<int:pk>/', MilestoneDetailAPIView.as_view(), name='milestone-detail'),
    # Endpoint for listing and creating notifications
    path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
]
