import time
from enum import Enum

from django.db import models

from project.models import Project
from user.models import User


class AuctionState(Enum):
    Waiting = 0
    InProgress = 1
    Canceled = 2
    Expired = 3
    Finished = 4


# Create your models here.
class Auction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    end_time = models.IntegerField(default=int(time.time()))
    start_time = models.IntegerField(default=int(time.time()))
    sale_token_num = models.IntegerField(default=1)
    minimum_value_per_token = models.IntegerField(default=1)
    state = models.IntegerField(choices=[(tag, tag.value) for tag in AuctionState],
                                default=AuctionState.Waiting.value)

    def get_auction_state(self):
        pass


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    token_num = models.IntegerField()


class Winner(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bought_token = models.IntegerField()
    total_value = models.IntegerField()
    transaction_hash = models.CharField(max_length=500)
