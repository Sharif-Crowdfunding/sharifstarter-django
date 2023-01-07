from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from auction.serializers import *


# Create your views here.
class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuctionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        a= Auction()
        return Response(AuctionSerializer(a).data)