from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class VoiceCommand(models.Model):
    """Model for storing voice commands"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_commands')
    command_text = models.TextField()
    audio_file = models.FileField(upload_to='voice_commands/', blank=True, null=True)
    transcription = models.TextField()
    intent = models.CharField(max_length=100)
    confidence = models.FloatField()
    processed_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-processed_at']
        indexes = [
            models.Index(fields=['user', 'intent']),
            models.Index(fields=['processed_at']),
        ]


class OCRReceipt(models.Model):
    """Model for OCR-processed receipts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ocr_receipts')
    image = models.ImageField(upload_to='receipts/ocr/')
    extracted_data = JSONField(default=dict)
    confidence_score = models.FloatField()
    processed_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-processed_at']
        indexes = [
            models.Index(fields=['user', 'processed_at']),
        ]


class VoiceAssistantSession(models.Model):
    """Model for voice assistant sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    context = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', 'session_id']),
            models.Index(fields=['is_active']),
        ]
