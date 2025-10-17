from django.urls import path, include
from  . import views
from rest_framework import routers, serializers, viewsets
#from soumission.views import UserViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from .views import RegisterView, ProfileView

# Ici nous créons notre routeur
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)



urlpatterns = [
    # URL de page d'acceuil
    path('',  views.home, name='home'),
    
    path('api/inscription_hackathon',  views.inscription_hackathon, name='inscription_hackathon'),
    path("api/hackathon/", views.hackathon_active, name="hackathon_active"),
    path("api/list/", views.hackathon_list, name="hackathon_list"),


    
    path('api/', include((router.urls, 'app_name'))),
    #path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #path("profile/", ProfileView.as_view(), name="profile"),

]


