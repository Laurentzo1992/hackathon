from django.shortcuts import render
from soumission.serializers  import UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets


def home(request):
    return render(request, 'soumission/home.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer