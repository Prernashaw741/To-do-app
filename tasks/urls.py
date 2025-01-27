from django.urls import path
from .views import TaskListCreateView, TaskDetailView, mark_completed, mark_important

urlpatterns = [
    path('add/', TaskListCreateView.as_view()),
    path('detail/<int:pk>/', TaskDetailView.as_view()),
    path('complete/<int:pk>/', mark_completed),
    path('important/<int:pk>/', mark_important)
]
