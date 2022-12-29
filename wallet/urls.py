from django.urls import path, include
from .views import WalletView

urlpatterns = [
    path('info/', WalletView.as_view()),
]
