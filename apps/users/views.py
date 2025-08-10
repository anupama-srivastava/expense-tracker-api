from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter users - only allow users to see their own data"""
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view requires."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """Create a new user"""
        serializer.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter profiles for the current user"""
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return UserProfileSerializer

    def perform_create(self, serializer):
        """Create a new user profile for the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "Profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Update current user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "Profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Custom user registration endpoint"""
    from .serializers import UserSerializer
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """Get detailed user information"""
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        profile_data = UserProfileSerializer(profile).data
    except UserProfile.DoesNotExist:
        profile_data = None
    
    return Response({
        'user': UserSerializer(user).data,
        'profile': profile_data
    })
