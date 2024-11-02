from django.urls import path
from comments import views

app_name = 'comments'  # Adding app_name for namespace

urlpatterns = [
    path('', views.CommentList.as_view(), name='comment-list'),
    path('<int:pk>/', views.CommentDetail.as_view(), name='comment-detail')
]
