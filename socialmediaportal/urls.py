from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('manager/admin/', admin.site.urls),
    path('', include('portal.urls')),
]

urlpatterns += staticfiles_urlpatterns()
