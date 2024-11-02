from django.urls import path
from posts import views

app_name = 'posts'  # Adding app_name for namespace

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail')
]
