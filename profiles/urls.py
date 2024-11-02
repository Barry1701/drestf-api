from django.urls import path
from profiles import views

app_name = 'profiles'  # Adding app_name for namespace

urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile-list'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
]
