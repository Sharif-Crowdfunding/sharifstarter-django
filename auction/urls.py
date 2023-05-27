from django.urls import path, include

from auction.views import *

urlpatterns = [
    path('create/', CreateAuctionView.as_view()),
    path('market/', GetAuctionList.as_view()),
    path('bid/', BidOnAuction.as_view()),
    path('details/<id>/', GetAuctionDetails.as_view()),
    path('bid/all/<id>/', GetAllBids.as_view()),
    path('mybid/<id>/', GetMyBid.as_view()),
    path('like/<id>/', LikeAuction.as_view()),
    path('cancel/<id>/', CancelAuction.as_view()),
    path('end/<id>/', CalcAuction.as_view())

]
