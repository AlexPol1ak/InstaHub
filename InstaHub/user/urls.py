
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

# uvicorn InstaHub.asgi:application --reload

urlpatterns = [
    path('test/', test_view),
    path('create-user/', CreateUserAPIView.as_view(), name='create_user'), #post
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  #post
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #post
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #post
    path('my-data/', RetrieveSelfUserAPIView.as_view(), name='my_data'), #get
    path('user-data/<int:pk>/', RetrieveUserAPIView.as_view(), name='user-data'), #get
    path('update-user/<int:pk>/', UdpadeUserDataAPIView.as_view(), name='update-user'), #put, patch
    path('update-password/<int:pk>/', UpdatePasswordAPIView.as_view(), name='update_password'), #put, patch




]
