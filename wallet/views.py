from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime

from auction.models import Auction
from project.models import Project
from utils.ethereum.blockchain import get_eth_provider
from wallet.models import CryptoWallet, TokenAsset


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        wallet.update_wallet()
        tokens = TokenAsset.objects.filter(wallet=wallet)
        auction_count = len(Auction.objects.filter(creator=request.user))
        project_count = len(Project.objects.filter(user=request.user))
        res = {
            'address': wallet.address,
            'balance': wallet.get_balance(),
            'auction_number':auction_count,
            'project_number':project_count,
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
            "reciever_address":"0xb7e0DBa2a0EB6F9eC0F8a30Bb09afCb0A7baC58F",
            "token_name":"PMP",
            "price":"200000",
            "project":"طراحی پمپ آب هوشمند",
            "status":"در حال انجام"
        }
        return Response(res)