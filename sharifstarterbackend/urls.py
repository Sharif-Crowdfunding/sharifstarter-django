from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('user.urls')),
    path('admin/', admin.site.urls),
]
