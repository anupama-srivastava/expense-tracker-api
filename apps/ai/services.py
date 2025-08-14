import numpy as np
from datetime import datetime, timedelta
from django.db.models import Sum, Avg, Count
from django.utils import timezone
import pandas as pd

from apps.expenses.models import Expense, Category
from .models import AIExpensePrediction, UserSpendingPattern, SmartBudgetRecommendation, AnomalyAlert


class AIPredictionService:
    """Service for AI-powered expense predictions"""
    
    def __init__(self, user):
        self.user = user
    
    def generate_predictions(self):
        """Generate expense predictions based on historical data"""
        # Get user's last 3 months of expenses
        three_months_ago = timezone.now() - timedelta(days=90)
        expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__gte=three_months_ago
        )
        
        if not expenses.exists():
            return []
        
        # Calculate patterns
        category_spending = expenses.values('category__name').annotate(
            total=Sum('amount'),
            avg=Avg('amount'),
            count=Count('id')
        )
        
        predictions = []
        
        for category_data in category_spending:
            category_name = category_data['category__name']
            avg_amount = float(category_data['avg'])
            
            # Predict next month's spending
            predicted_amount = avg_amount * 4  # Assuming weekly pattern
            
            prediction = AIExpensePrediction.objects.create(
                user=self.user,
                category=category_name,
                predicted_amount=predicted_amount,
                prediction_date=timezone.now().date() + timedelta(days=30),
                confidence_score=0.85,
                features_used={
                    'avg_amount': avg_amount,
                    'count': category_data['count'],
                    'total': float(category_data['total'])
                }
            )
            predictions.append(prediction)
        
        return predictions
    
    def get_spending_forecast(self, days=30):
        """Get spending forecast for the next N days"""
        predictions = AIExpensePrediction.objects.filter(
            user=self.user,
            prediction_date__gte=timezone.now().date(),
            prediction_date__lte=timezone.now().date() + timedelta(days=days)
        )
        
        total_forecast = predictions.aggregate(
            total=Sum('predicted_amount')
        )['total'] or 0
        
        return {
            'total_forecast': float(total_forecast),
            'predictions': list(predictions.values()),
            'period': days
        }


class AIChatService:
    """Service for AI chat functionality"""
    
    def __init__(self, user):
        self.user = user
    
    def process_message(self, message, context=None):
        """Process user message and return AI response"""
        context = context or {}
        
        # Simple NLP processing (in production, use proper NLP library)
        message_lower = message.lower()
        
        if 'spending' in message_lower and 'this month' in message_lower:
            return self._handle_spending_query()
        elif 'budget' in message_lower and 'recommend' in message_lower:
            return self._handle_budget_recommendation()
        elif 'anomaly' in message_lower or 'unusual' in message_lower:
            return self._handle_anomaly_detection()
        elif 'predict' in message_lower or 'forecast' in message_lower:
            return self._handle_prediction_query()
        else:
            return {
                'response': "I can help you with spending analysis, budget recommendations, anomaly detection, and spending predictions. What would you like to know?",
                'action': 'help',
                'data': {}
            }
    
    def _handle_spending_query(self):
        """Handle spending-related queries"""
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__month=current_month,
            transaction_date__year=current_year
        )
        
        total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        category_breakdown = expenses.values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')[:5]
        
        return {
            'response': f"You've spent ${total_spent:.2f} this month. Your top categories are: {', '.join([f'{c['category__name']}: ${c['total']:.2f}' for c in category_breakdown])}",
            'action': 'spending_summary',
            'data': {
                'total_spent': float(total_spent),
                'category_breakdown': list(category_breakdown)
            }
        }
    
    def _handle_budget_recommendation(self):
        """Handle budget recommendation requests"""
        service = AIInsightsService(self.user)
        recommendations = service.generate_budget_recommendations()
        
        return {
            'response': f"I've analyzed your spending patterns and have {len(recommendations)} budget recommendations for you.",
            'action': 'budget_recommendations',
            'data': {'recommendations': recommendations}
        }
    
    def _handle_anomaly_detection(self):
        """Handle anomaly detection requests"""
        service = AIInsightsService(self.user)
        anomalies = service.detect_anomalies()
        
        if anomalies:
            return {
                'response': f"I found {len(anomalies)} unusual spending patterns. Would you like me to show you the details?",
                'action': 'anomaly_list',
                'data': {'anomalies': anomalies}
            }
        else:
            return {
                'response': "No unusual spending patterns detected in your recent transactions.",
                'action': 'no_anomalies',
                'data': {}
            }
    
    def _handle_prediction_query(self):
        """Handle prediction-related queries"""
        service = AIPredictionService(self.user)
        forecast = service.get_spending_forecast()
        
        return {
            'response': f"Based on your spending patterns, I predict you'll spend approximately ${forecast['total_forecast']:.2f} in the next 30 days.",
            'action': 'spending_forecast',
            'data': forecast
        }


class AIInsightsService:
    """Service for generating AI insights"""
    
    def __init__(self, user):
        self.user = user
    
    def get_quick_insights(self):
        """Get quick insights about user's spending"""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Current month insights
        expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__gte=month_start
        )
        
        total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        # Compare with last month
        last_month_start = (month_start - timedelta(days=30)).replace(day=1)
        last_month_end = month_start - timedelta(days=1)
        
        last_month_expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__gte=last_month_start,
            transaction_date__lte=last_month_end
        )
        
        last_month_total = last_month_expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate percentage change
        if last_month_total > 0:
            change_percent = ((total_spent - last_month_total) / last_month_total) * 100
        else:
            change_percent = 0
        
        # Top spending category
        top_category = expenses.values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total').first()
        
        insights = {
            'total_spent_this_month': float(total_spent),
            'change_from_last_month': float(change_percent),
            'top_category': top_category['category__name'] if top_category else None,
            'top_category_amount': float(top_category['total']) if top_category else 0,
            'expense_count': expenses.count(),
            'average_expense': float(total_spent / max(expenses.count(), 1))
        }
        
        return insights
    
    def generate_budget_recommendations(self):
        """Generate smart budget recommendations"""
        # Get user's spending patterns
        three_months_ago = timezone.now() - timedelta(days=90)
        expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__gte=three_months_ago
        )
        
        recommendations = []
        
        for category in Category.objects.all():
            category_expenses = expenses.filter(category=category)
            if category_expenses.exists():
                avg_monthly = category_expenses.aggregate(
                    avg=Avg('amount')
                )['avg'] or 0
                
                # Calculate recommended budget (20% buffer)
                recommended = avg_monthly * 4 * 1.2
                
                recommendation = SmartBudgetRecommendation.objects.create(
                    user=self.user,
                    category=category.name,
                    recommended_amount=recommended,
                    current_spending=avg_monthly * 4,
                    reasoning=f"Based on your average monthly spending of ${avg_monthly * 4:.2f} in {category.name}",
                    confidence_level=0.85
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def detect_anomalies(self):
        """Detect unusual spending patterns"""
        # Get last 30 days of expenses
        thirty_days_ago = timezone.now() - timedelta(days=30)
        expenses = Expense.objects.filter(
            user=self.user,
            transaction_date__gte=thirty_days_ago
        )
        
        anomalies = []
        
        for expense in expenses:
            # Calculate z-score for this expense
            category_expenses = Expense.objects.filter(
                user=self.user,
                category=expense.category,
                transaction_date__gte=thirty_days_ago
            ).exclude(id=expense.id)
            
            if category_expenses.exists():
                amounts = list(category_expenses.values_list('amount', flat=True))
                mean = np.mean(amounts)
                std = np.std(amounts)
                
                if std > 0:
                    z_score = abs((float(expense.amount) - mean) / std)
                    
                    if z_score > 2:  # More than 2 standard deviations
                        anomaly = AnomalyAlert.objects.create(
                            user=self.user,
                            expense=expense,
                            anomaly_score=z_score,
                            expected_range={'min': float(mean - 2*std), 'max': float(mean + 2*std)},
                            actual_amount=expense.amount
                        )
                        anomalies.append(anomaly)
        
        return anomalies
