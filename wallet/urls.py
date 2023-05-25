from django.urls import path, include
from .views import *

urlpatterns = [
    path('info/', WalletView.as_view()),
    path('credit/', GetCreditView.as_view()),
    path('trasactions/', GetTransactionView.as_view()),
]
