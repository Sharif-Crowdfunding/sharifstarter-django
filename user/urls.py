from django.urls import path, include
from .views import RegisterView, UserView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    # path('login', LoginView.as_view()),
    path('info/', UserView.as_view()),
    # path('logout', LogoutView.as_view()),
]
