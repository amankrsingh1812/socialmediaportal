
from django.contrib import admin
from django.urls import path, include
from . import views

appname="portal"

urlpatterns = [
    path(r'dashboard/',views.home1),
    path(r'admin/',views.home3),
    path(r'dashboard1/',views.home2),
    path(r'dashboard1/<pname>', views.home4),
    path(r'login/',views.login_user),
    path(r'logout/',views.logout1),
    path(r'output/',views.output),
]
