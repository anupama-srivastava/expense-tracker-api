from rest_framework import serializers
from .models import VoiceCommand, OCRReceipt, VoiceAssistantSession


class VoiceCommandSerializer(serializers.ModelSerializer):
    """Serializer for VoiceCommand model"""
    
    class Meta:
        model = VoiceCommand
        fields = [
            'id', 'user', 'command_text', 'transcription', 'intent', 'confidence',
            'is_processed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class OCRReceiptSerializer(serializers.ModelSerializer):
    """Serializer for OCRReceipt model"""
    
    class Meta:
        model = OCRReceipt
        fields = [
            'id', 'user', 'image', 'extracted_data', 'confidence_score',
            'is_processed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for VoiceAssistantSession model"""
    
    class Meta:
        model = VoiceAssistantSession
        fields = [
            'id', 'user', 'session_id', 'start_time', 'end_time', 'context',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
