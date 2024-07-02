# from django.urls import path
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.whatsapp.api import views
from apps.whatsapp.api.views import WhatsappBotApi, webhook

router = DefaultRouter()
router.register("whatsapp_bot", WhatsappBotApi, basename="whatsapp bot")

urlpatterns = [path("whatsappwebhook", views.webhook, name="WebHook")] + router.urls
