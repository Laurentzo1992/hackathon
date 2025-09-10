from django.urls import path, include
from  . import views
from rest_framework import routers, serializers, viewsets
from soumission.views import UserViewSet

# Ici nous créons notre routeur
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    path('',  views.home, name='home'),
    path('api/', include((router.urls, 'app_name')))

]


