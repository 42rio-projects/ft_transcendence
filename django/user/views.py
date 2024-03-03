from django.shortcuts import render
from rest_framework import viewsets, permissions
import user.serializers as serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
# Create your views here.
