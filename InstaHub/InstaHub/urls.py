
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/parser/', include('parser.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/doc/', include('APIDoc.urls')),
    # re_path(r'^.*/$', error404, name='error404'),
]
