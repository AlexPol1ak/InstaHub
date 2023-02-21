from django.urls import path, include
from .views import *
from rest_framework import routers

urlpatterns = [
    path('test-parser/', test_view_parser),
    ]