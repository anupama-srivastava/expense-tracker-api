from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import InvestmentAccount, Asset, Portfolio, Transaction, Performance, Goal
from .serializers import (
    InvestmentAccountSerializer, AssetSerializer, PortfolioSerializer,
    TransactionSerializer, PerformanceSerializer, GoalSerializer
)

# Create your views here.
