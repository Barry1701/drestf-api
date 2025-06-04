from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("messages", views.DirectMessageViewSet, basename="message")

urlpatterns = [
    path("inbox/", views.InboxListCreate.as_view()),
    path("outbox/", views.OutboxList.as_view()),
]

urlpatterns += router.urls
