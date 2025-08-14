from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Import viewsets
from apps.analytics.views import AnalyticsReportViewSet, UserInsightViewSet, CategoryAnalyticsViewSet
from apps.users.views import UserViewSet
from apps.expenses.views import ExpenseViewSet
from apps.budgets.views import BudgetViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'reports', AnalyticsReportViewSet, basename='analytics-report')
router.register(r'insights', UserInsightViewSet, basename='user-insight')
router.register(r'categories', CategoryAnalyticsViewSet, basename='category-analytics')
router.register(r'users', UserViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/expenses/', include('apps.expenses.urls')),
    path('api/v1/budgets/', include('apps.budgets.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/social/', include('apps.social.urls')),
    pathNow let me update the main URLs configuration to include the WebSocket routing for the analytics app:

<edit_file>
<path>C:/Users/nupur/Desktop/expense-tracker-api/config/urls.py</path>
<content>
<<<<<<< SEARCH
from django.urls import path, include
=======
from django.urls import path, include, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from apps.analytics.routing import websocket_urlpatterns
>>>>>>> REPLACE
# Import viewsets
from apps.banking.views import BankAccountViewSet, TransactionViewSet, TransactionCategoryViewSet, SyncLogViewSet
from apps.investments.views import InvestmentAccountViewSet, AssetViewSet, PortfolioViewSet, TransactionViewSet as InvestmentTransactionViewSet, PerformanceViewSet, GoalViewSet
from apps.crypto.views import ExchangeViewSet, CryptoAssetViewSet, WalletViewSet, CryptoHoldingViewSet, CryptoTransactionViewSet, StakingRewardViewSet, PriceHistoryViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'bank-accounts', BankAccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transaction-categories', TransactionCategoryViewSet)
router.register(r'sync-logs', SyncLogViewSet)
router.register(r'investment-accounts', InvestmentAccountViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'portfolios', PortfolioViewSet)
router.register(r'investment-transactions', InvestmentTransactionViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'exchanges', ExchangeViewSet)
router.register(r'crypto-assets', CryptoAssetViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'crypto-holdings', CryptoHoldingViewSet)
router.register(r'crypto-transactions', CryptoTransactionViewSet)
router.register(r'staking-rewards', StakingRewardViewSet)
router.register(r'price-history', PriceHistoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # WebSocket URLs
    re_path(r'ws/analytics/', include(websocket_urlpatterns)),
]
