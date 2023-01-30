import datetime
import time
import calendar
from enum import Enum

from django.db import models
from django.utils.timezone import now

from project.models import Project
from user.models import User
from utils.ethereum.blockchain import get_eth_provider


class AuctionState(Enum):
    Waiting = 0
    InProgress = 1
    Canceled = 2
    Finished = 3


# Create your models here.
class Auction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    end_time = models.IntegerField(default=int(time.time()))
    start_time = models.IntegerField(default=int(time.time()))
    sale_token_num = models.IntegerField(default=1)
    minimum_value_per_token = models.IntegerField(default=1)
    contract_address = models.CharField(default="", max_length=100)
    state = models.IntegerField(choices=[(tag, tag.value) for tag in AuctionState],
                                default=AuctionState.Waiting.value)

    def get_auction_state(self):
        eth_p = get_eth_provider()
        auction = eth_p.get_auction(contract_address=self.contract_address)
        auction.updateState()
        # date = datetime.datetime.utcnow()
        # utc_time = calendar.timegm(date.utctimetuple())
        # if self.state == 0 and self.start_time>

    def get_bidding_time(self):
        return self.end_time - self.start_time


class LikedAuction(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.Model)


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    token_num = models.IntegerField(default=0)
    total_val = models.BigIntegerField(default=0)


class Winner(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bought_token = models.IntegerField()
    total_value = models.IntegerField()
    transaction_hash = models.CharField(max_length=500)
