import datetime
import math

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from auction.serializers import *
from utils.ethereum.blockchain import get_eth_provider


# Create your views here.
class CreateAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        validated = False
        start_time = math.floor(datetime.datetime.timestamp(datetime.datetime.utcnow()))
        end_time = start_time + data['duration']
        if data['minimum_value_per_token'] > 10000 and data['sale_token_num'] > 0:
            if start_time < end_time:
                validated = True
        if not validated:
            return Response(status=HTTP_400_BAD_REQUEST)
        p = Project.objects.get(token_info__symbol=data['symbol'])
        a = Auction(project=p, creator=user, start_time=start_time, end_time=end_time,
                    sale_token_num=data['sale_token_num'], minimum_value_per_token=data['minimum_value_per_token'])

        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(user.wallet.encrypted_private_key, user.username)
        result = eth_p.get_project(p.contract_address).create_auction(user.wallet.address, pk, a.sale_token_num,
                                                                      a.minimum_value_per_token, a.get_bidding_time())
        auctions = eth_p.get_project(p.contract_address).get_auctions()
        a.contract_address = auctions[-1]

        a.creator.wallet.update_wallet()
        a.save()
        return Response(AuctionSerializer(a).data)


class GetAuctionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auctions = Auction.objects.all()
        res = []
        for a in auctions:
            temp = {
                'minimum_bid_per_token': a.minimum_value_per_token,
                'sale_token_num': a.sale_token_num,
                'id': a.id,
                'creator': a.creator.username,
                'project': {
                    'symbol': a.project.token_info.symbol,
                    'image': a.project.image,
                    'creator': a.project.user.username,
                    'id': a.project.id
                },
                'is_liked': len(LikedAuction.objects.filter(auction=a, user=request.user)) > 0,
                'bidders': [BidSerializer(b).data for b in Bid.objects.filter(auction=a)],
                'end_time': a.end_time,
                'is_ended': a.state == AuctionState.Finished.value,
                'is_canceled': a.state == AuctionState.Canceled.value
            }
            res.append(temp)
        return Response(data=res, status=HTTP_200_OK)


class LikeAuction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        auction = Auction.objects.get(id=id)
        if not auction:
            return Response(status=HTTP_404_NOT_FOUND)
        LikedAuction.objects.create(auction=auction, user=request.user)
        return Response(HTTP_200_OK)


class CalcAuction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        auction = Auction.objects.get(id=id)
        if not auction:
            return Response(status=HTTP_404_NOT_FOUND)
        if auction.creator != request.user:
            return Response(status=HTTP_401_UNAUTHORIZED)
        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(request.user.wallet.encrypted_private_key, request.user.username)


        result = eth_p.get_project(auction.project.contract_address).calc_auction(request.user.wallet.address, pk,
                                                                                  auction.contract_address)
        print(result)
        auction.calc_result()
        return Response(HTTP_200_OK)


class CancelAuction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        auction = Auction.objects.get(id=id)
        if not auction:
            return Response(status=HTTP_404_NOT_FOUND)
        if auction.creator != request.user:
            return Response(status=HTTP_401_UNAUTHORIZED)
        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(request.user.wallet.encrypted_private_key, request.user.username)
        result = eth_p.get_project(auction.project.contract_address).cancel_auction(request.user.wallet.address, pk,
                                                                                  auction.contract_address)
        print(result)
        auction.cancel()
        return Response(HTTP_200_OK)

class GetAuctionDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        a = Auction.objects.get(id=int(id))
        if not a:
            return Response(status=HTTP_404_NOT_FOUND)

        res = {
            'minimum_bid_per_token': a.minimum_value_per_token,
            'sale_token_num': a.sale_token_num,
            'end_time': a.end_time,
            'start_time': a.start_time,
            'id': a.id,
            'project': {
                'symbol': a.project.token_info.symbol,
                'website': a.project.basic_info.website,
                'telegram_id':a.project.basic_info.telegram_id,
                'details': a.project.basic_info.details,
                'github_id': a.project.basic_info.github_id,
                'image': a.project.image,
                'creator': a.project.user.username,
                'id': a.project.id
            },
            'bidders': [BidSerializer(b).data for b in Bid.objects.filter(auction=a)]
        }
        return Response(data=res, status=HTTP_200_OK)


class BidOnAuction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        auction = Auction.objects.get(id=data['id'])
        b = Bid(bidder=user, auction=auction, token_num=data['token_num'], total_val=data['total_val'])
        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(user.wallet.encrypted_private_key, user.username)
        print(eth_p.get_auction(auction.contract_address).update_state(user.wallet.address, pk))
        print(eth_p.get_auction(auction.contract_address).get_timestamp())
        print(eth_p.get_auction(auction.contract_address).get_state())
        result = eth_p.get_auction(auction.contract_address).bid(user.wallet.address, pk, b.token_num, b.total_val)

        print(result)
        b.save()
        return Response(BidSerializer(b).data, status=HTTP_200_OK)


class GetMyBid(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        print(id)
        bids = Bid.objects.filter(auction__id=id, bidder=request.user)
        print(bids)
        res = []
        for bid in bids:
            temp = {
                "bidder": bid.bidder.username,
                "auction_id": bid.auction.id,
                "total_val": bid.total_val,
                "token_num": bid.token_num,
                "token_val": bid.total_val / bid.token_num
            }
            res.append(temp)
        return Response(res)


class GetAllBids(APIView):
    def get(self, request, id):
        print(id)
        Bids = Bid.objects.filter(auction__id=id)
        res = []
        for bid in Bids:
            res.append(BidSerializer(bid).data)
        return Response(res)