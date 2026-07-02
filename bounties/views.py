from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Bounty
from .serializers import RegisterSerializer, BountySerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


def _bounty_cache_key(user_id):
    return f'bounty_list_{user_id}'


class BountyListCreateView(generics.ListCreateAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bounty.objects.filter(owner=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        cache_key = _bounty_cache_key(request.user.id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.delete(_bounty_cache_key(self.request.user.id))


class BountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bounty.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(_bounty_cache_key(self.request.user.id))

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(_bounty_cache_key(self.request.user.id))