from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

from .models import AIExpensePrediction, UserSpendingPattern, SmartBudgetRecommendation, AnomalyAlert
from .serializers import (
    AIExpensePredictionSerializer, 
    UserSpendingPatternSerializer,
    SmartBudgetRecommendationSerializer,
    AnomalyAlertSerializer,
    AIChatRequestSerializer,
    AIChatResponseSerializer
)


class AIExpensePredictionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AI-powered expense predictions
    """
    queryset = AIExpensePrediction.objects.all()
    serializer_class = AIExpensePredictionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'prediction_date', 'confidence_score']
    search_fields = ['category', 'user__email']
    ordering_fields = ['predicted_amount', 'confidence_score', 'created_at']

    def get_queryset(self):
        return AIExpensePrediction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming_predictions(self, request):
        """Get upcoming expense predictions for the next 7 days"""
        predictions = self.get_queryset().filter(
            prediction_date__gte=timezone.now().date(),
            prediction_date__lte=timezone.now().date() + timedelta(days=7)
        ).order_by('prediction_date')
        
        serializer = self.get_serializer(predictions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def generate_predictions(self, request):
        """Generate AI predictions for user's spending patterns"""
        # This would integrate with actual ML model
        # For now, returning mock data
        from .services import AIPredictionService
        
        service = AIPredictionService(request.user)
        predictions = service.generate_predictions()
        
        return Response({
            'message': 'Predictions generated successfully',
            'predictions': predictions
        })


class UserSpendingPatternViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user spending patterns
    """
    queryset = UserSpendingPattern.objects.all()
    serializer_class = UserSpendingPatternSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'day_of_week', 'time_of_day']
    ordering_fields = ['amount', 'created_at']

    def get_queryset(self):
        return UserSpendingPattern.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def weekly_patterns(self, request):
        """Get spending patterns for the current week"""
        patterns = self.get_queryset().filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id'),
            avg_amount=Avg('amount')
        )
        
        return Response(patterns)


class SmartBudgetRecommendationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AI-generated budget recommendations
    """
    queryset = SmartBudgetRecommendation.objects.all()
    serializer_class = SmartBudgetRecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_accepted']
    ordering_fields = ['recommended_amount', 'confidence_level']

    def get_queryset(self):
        return SmartBudgetRecommendation.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pending_recommendations(self, request):
        """Get pending budget recommendations"""
        recommendations = self.get_queryset().filter(is_accepted=False)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept_recommendation(self, request, pk=None):
        """Accept a budget recommendation"""
        recommendation = self.get_object()
        recommendation.is_accepted = True
        recommendation.save()
        
        return Response({
            'message': 'Recommendation accepted successfully',
            'recommendation': self.get_serializer(recommendation).data
        })


class AnomalyAlertViewSet(viewsets.ModelViewSet):
    """
    ViewSet for anomaly alerts
    """
    queryset = AnomalyAlert.objects.all()
    serializer_class = AnomalyAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_investigated']
    ordering_fields = ['anomaly_score', 'created_at']

    def get_queryset(self):
        return AnomalyAlert.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent_alerts(self, request):
        """Get recent anomaly alerts (last 30 days)"""
        alerts = self.get_queryset().filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).order_by('-anomaly_score')
        
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_investigated(self, request, pk=None):
        """Mark an anomaly alert as investigated"""
        alert = self.get_object()
        alert.is_investigated = True
        alert.save()
        
        return Response({
            'message': 'Alert marked as investigated',
            'alert': self.get_serializer(alert).data
        })


class AIChatViewSet(viewsets.ViewSet):
    """
    ViewSet for AI chat functionality
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Handle AI chat requests"""
        serializer = AIChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            from .services import AIChatService
            
            chat_service = AIChatService(request.user)
            response = chat_service.process_message(
                serializer.validated_data['message'],
                serializer.validated_data.get('context', {})
            )
            
            return Response(AIChatResponseSerializer(response).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def quick_insights(self, request):
        """Get quick AI insights about user's spending"""
        from .services import AIInsightsService
        
        insights_service = AIInsightsService(request.user)
        insights = insights_service.get_quick_insights()
        
        return Response(insights)
