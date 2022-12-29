from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('info/', UserView.as_view()),
    path('update-password/',UpdatePassword.as_view()),
    path('logout/', LogoutView.as_view()),
]

