from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import VoiceCommand, OCRReceipt, VoiceAssistantSession
from .serializers import VoiceCommandSerializer, OCRReceiptSerializer, VoiceAssistantSessionSerializer
from .services import VoiceCommandService, OCRService, VoiceAssistantService


class VoiceCommandViewSet(viewsets.ModelViewSet):
    """ViewSet for managing voice commands"""
    queryset = VoiceCommand.objects.all()
    serializer_class = VoiceCommandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VoiceCommand.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def process_command(self, request):
        """Process a voice command"""
        serializer = VoiceCommandSerializer(data=request.data)
        if serializer.is_valid():
            command_text = serializer.validated_data.get('command_text')
            audio_file = request.FILES.get('audio_file')
            
            service = VoiceCommandService(request.user)
            result = service.process_voice_command(audio_file, command_text)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def recent_commands(self, request):
        """Get recent voice commands"""
        recent_commands = self.get_queryset().filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_commands, many=True)
        return Response(serializer.data)


class OCRReceiptViewSet(viewsets.ModelViewSet):
    """ViewSet for managing OCR receipts"""
    queryset = OCRReceipt.objects.all()
    serializer_class = OCRReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OCRReceipt.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def process_receipt(self, request):
        """Process an OCR receipt"""
        serializer = OCRReceiptSerializer(data=request.data)
        if serializer.is_valid():
            image_file = request.FILES.get('image')
            
            if not image_file:
                return Response(
                    {'error': 'Image file is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = OCRService(request.user)
            result = service.process_receipt_image(image_file)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def recent_receipts(self, request):
        """Get recent OCR receipts"""
        recent_receipts = self.get_queryset().filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_receipts, many=True)
        return Response(serializer.data)


class VoiceAssistantSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing voice assistant sessions"""
    queryset = VoiceAssistantSession.objects.all()
    serializer_class = VoiceAssistantSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VoiceAssistantSession.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_session(self, request):
        """Create a new voice assistant session"""
        service = VoiceAssistantService(request.user)
        context = request.data.get('context', {})
        
        session = service.create_session(context)
        serializer = self.get_serializer(session)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def process_message(self, request, pk=None):
        """Process a message within a session"""
        session = self.get_object()
        message = request.data.get('message')
        
        if not message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = VoiceAssistantService(request.user)
        response = service.process_session_message(session.session_id, message)
        
        return Response(response)

    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End a voice assistant session"""
        session = self.get_object()
        service = VoiceAssistantService(request.user)
        
        if service.end_session(session.session_id):
            session.refresh_from_db()
            serializer = self.get_serializer(session)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Failed to end session'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def active_sessions(self, request):
        """Get active voice assistant sessions"""
        active_sessions = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_sessions, many=True)
        return Response(serializer.data)
