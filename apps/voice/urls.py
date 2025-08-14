from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoiceCommandViewSet, OCRReceiptViewSet, VoiceAssistantSessionViewSet

router = DefaultRouter()
router.register(r'commands', VoiceCommandViewSet, basename='voice-commands')
router.register(r'ocr', OCRReceiptViewSet, basename='ocr-receipts')
router.register(r'sessions', VoiceAssistantSessionViewSet, basename='voice-sessions')

urlpatterns = [
    path('', include(router.urls)),
]
