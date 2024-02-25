from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/auth/token/login/', views.obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # url(r'^auth/', include('djoser.urls')),
    # url(r'^auth/', include('djoser.urls.authtoken')),
]
