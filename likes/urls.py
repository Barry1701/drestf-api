from django.urls import path
from likes import views

app_name = 'likes'  # Adding app_name for namespace

urlpatterns = [
    path('', views.LikeList.as_view(), name='like-list'),
    path('<int:pk>/', views.LikeDetail.as_view(), name='like-detail'),
]
