
from django.contrib import admin
from django.urls import path, include
from . import views

appname="portal"

urlpatterns = [
    path(r'dashboard/',views.home1),
    path(r'login/',views.login_user),
    path(r'logout/',views.logout1),
]
