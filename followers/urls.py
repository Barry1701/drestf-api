from django.urls import path
from followers import views

app_name = 'followers'  # Adding app_name for namespace

urlpatterns = [
    path('', views.FollowerList.as_view(), name='follower-list'),
    path('<int:pk>/', views.FollowerDetail.as_view(), name='follower-detail')
]
