from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'inst-account', ServiceInstagramAccountViewSet, basename='inst-account_service')
# print(router.urls)


urlpatterns = [
    path('test-parser/', test_view_parser),
    path('add-tracked-user/', AddTrackedUserAPIView.as_view(), name='add_tracked_user')
    ]

urlpatterns += router.urls