from django.urls import path
from . import views

urlpatterns = [
    path("inbox/", views.InboxListCreate.as_view()),
    path("outbox/", views.OutboxList.as_view()),
    path("messages/<int:pk>/", views.DirectMessageDetail.as_view()),
]
