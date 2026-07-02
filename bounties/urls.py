from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, BountyListCreateView, BountyDetailView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('bounties/', BountyListCreateView.as_view(), name='bounty-list-create'),
    path('bounties/<int:pk>/', BountyDetailView.as_view(), name='bounty-detail'),
]