from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
]
