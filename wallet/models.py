import json

from django.db import models

from utils.web3provider import Web3Provider


# Create your models here.
class CryptoWallet(models.Model):
    address = models.CharField(max_length=100)
    encrypted_private_key = models.CharField(max_length=600)
    eth_balance = models.BigIntegerField()

    def get_balance(self):
        current_balance = Web3Provider.web3.eth.getBalance(self.address)
        self.eth_balance = current_balance
        self.save()
        return current_balance


def create_wallet(password):
    address, account_encrypt = Web3Provider.create_eth_account(password)
    encrypted = json.dumps(account_encrypt)
    c = CryptoWallet(address=address, encrypted_private_key=encrypted, eth_balance=0)
    c.save()
    return c


class TokenAsset(models.Model):
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    contract_address = models.CharField(max_length=500)
    balance = models.BigIntegerField()
