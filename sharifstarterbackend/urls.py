from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user/', include('user.urls')),
    path('wallet/', include('wallet.urls')),
    path('project/', include('project.urls')),
    path('auction/', include('auction.urls')),
    path('report/', include('report.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
