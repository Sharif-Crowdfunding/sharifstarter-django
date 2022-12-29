import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.courier_email import send_email
from .models import User
from .serializers import UserSerializer


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # send_email()
        user = User.objects.filter(id=request.GET['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
