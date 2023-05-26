from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime

from utils.ethereum.blockchain import get_eth_provider
from wallet.models import CryptoWallet, TokenAsset


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        tokens = TokenAsset.objects.filter(wallet=wallet)
        res = {
            'address': wallet.address,
            'balance': wallet.get_balance(),
            'tokens': [{'symbol': t.symbol,'contract_address':t.contract_address, 'balance': t.balance} for t in tokens]
        }
        return Response(res)
class GetCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        result = get_eth_provider().get_credit(wallet.address,10)
        print(result)
        tokens = TokenAsset.objects.filter(wallet=wallet)
        res = {
            'address': wallet.address,
            'balance': wallet.get_balance(),
            'tokens': [{'symbol': t.symbol,'contract_address':t.contract_address, 'balance': t.balance} for t in tokens]
        }
        return Response(res)

class GetTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        res = {
            "date":str(datetime.datetime.now()),
            "value":""
        }
        return Response(res)