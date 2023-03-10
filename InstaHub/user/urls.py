
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

# uvicorn InstaHub.asgi:application --reload


router = routers.SimpleRouter()
router.register(r'inst-account', UserInstagramAccountViewSet, basename='inst-account')
# print(router.urls)


urlpatterns = [
    path('test/', test_view),
    path('create-user/', CreateUserAPIView.as_view(), name='create_user'), #post
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  #post
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #post
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #post
    path('my-data/', RetrieveSelfUserAPIView.as_view(), name='my_data'), #get
    path('user-data/<int:pk>/', RetrieveUserAPIView.as_view(), name='user-data'), #get
    path('update-user/<int:pk>/', UdpadeUserDataAPIView.as_view(), name='update-user'), #put, patch
    path('update-password/<int:pk>/', UpdatePasswordAPIView.as_view(), name='update_password'), #put, patch
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'), #post
    path('get-all-users/', GetAllUsersAPIView.as_view(), name='get_all_users'), #get
    path('self-delete/', DestroySelfAPIView.as_view(), name='self-delete'), #delete
    path('self-deactivate/', DeactivateSelfAPIView.as_view(), name='self-deactivate'), #delete
    path('delete-user/<int:pk>/', DestroyUserAPIView.as_view(), name='delete-user'), #delete
    path('deactivate-user/<int:pk>/', DeactivateUserAPIView.as_view(), name='delete-user'), #delete
    path('all-user-data/', RetrieveSelfAllUserDataAPIView.as_view(), name='all_user_data'), #get

]

urlpatterns += router.urls
