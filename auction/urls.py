from django.urls import path, include

from auction.views import *

urlpatterns = [
    path('create/', CreateAuctionView.as_view()),
    path('market/', GetAuctionList.as_view()),
    path('bid/', BidOnAuction.as_view()),
    path('details/<id>/', GetAuctionDetails.as_view()),

]