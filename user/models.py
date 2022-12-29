from django.db import models
from django.contrib.auth.models import AbstractUser

from wallet.models import CryptoWallet


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE, default=None)
