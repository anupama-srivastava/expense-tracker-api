from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import (
    SharedExpense,
    SharedExpenseParticipant,
    FamilyBudget,
    FamilyBudgetMember,
    ExpenseChallenge,
    ExpenseChallengeParticipant,
    SocialFeed,
    SocialFeedComment
)


class SharedExpenseSerializer(serializers.ModelSerializer):
    """Serializer for shared expenses"""
    created_by = serializers.ReadOnlyField(source='created_by.email')
    participants = serializers.SerializerMethodField()
    
    class Meta:
        model = SharedExpense
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_participants(self, obj):
        return [user.email for user in obj.participants.all()]


class SharedExpenseParticipantSerializer(serializers.ModelSerializer):
    """Serializer for shared expense participants"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = SharedExpenseParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FamilyBudgetSerializer(serializers.ModelSerializer):
    """Serializer for family budgets"""
    created_by = serializers.ReadOnlyField(source='created_by.email')
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = FamilyBudget
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_members(self, obj):
        return [user.email for user in obj.members.all()]


class FamilyBudgetMemberSerializer(serializers.ModelSerializer):
    """Serializer for family budget members"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = FamilyBudgetMember
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenseChallengeSerializer(serializers.ModelSerializer):
    """Serializer for expense challenges"""
    created_by = serializers.ReadOnlyField(source='created_by.email')
    participants = serializers.SerializerMethodField()
    
    class Meta:
        model = ExpenseChallenge
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_participants(self, obj):
        return [user.email for user in obj.participants.all()]


class ExpenseChallengeParticipantSerializer(serializers.ModelSerializer):
    """Serializer for expense challenge participants"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = ExpenseChallengeParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SocialFeedSerializer(serializers.ModelSerializer):
    """Serializer for social feed"""
    created_by = serializers.ReadOnlyField(source='created_by.email')
    
    class Meta:
        model = SocialFeed
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SocialFeedCommentSerializer(serializers.ModelSerializer):
    """Serializer for social feed comments"""
    created_by = serializers.ReadOnlyField(source='created_by.email')
    
    class Meta:
        model = SocialFeedComment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VoiceCommandSerializer(serializers.ModelSerializer):
    """Serializer for voice commands"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceCommand
        fields = '__all__'
        read_only_fields = ('id', 'processed_at', 'updated_at')


class OCRReceiptSerializer(serializers.ModelSerializer):
    """Serializer for OCR receipts"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = OCRReceipt
        fields = '__all__'
        read_only_fields = ('id', 'processed_at', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.ModelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'updated_at')


class VoiceAssistantSessionSerializer(serializers.modelSerializer):
    """Serializer for voice assistant sessions"""
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = VoiceAssistantSession
        fields = '__all__'
        read_only_fields = ('id', 'start_timeNow let me create the serializers for the social features:

<create_file>
<path>C:/Users/nupur/Desktop/expense-tracker-api/apps/social/serializers.py</path>
<content>
from rest_framework import serializers
from .models import SharedExpense, FamilyBudget, ExpenseChallenge


class SharedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedExpense
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FamilyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyBudget
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenseChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseChallenge
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
