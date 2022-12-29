from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wallet.models import CryptoWallet, TokenAsset


# Create your views here
class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        tokens = TokenAsset.objects.filter(wallet=wallet)
        res = {
            'address': wallet.address,
            'balance': wallet.get_balance(),
            'tokens': [{'contract_address': t.contract_address, 'balance': t.balance} for t in tokens]
        }
        return Response(res)
