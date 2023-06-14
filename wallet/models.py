import json

from django.db import models

from utils.ethereum.blockchain import get_eth_provider
from utils.web3provider import Web3Provider


# Create your models here.
class CryptoWallet(models.Model):
    address = models.CharField(max_length=100)
    encrypted_private_key = models.CharField(max_length=600)
    eth_balance = models.FloatField()

    def get_balance(self):
        current_balance = get_eth_provider().get_balance(self.address)
        self.eth_balance = current_balance
        self.save()
        return current_balance

    def credit(self):
        get_eth_provider()

    def update_balance_of_contract(self,contract_address):
        eth_p = get_eth_provider()
        balance = eth_p.get_project(contract_address).get_balance(self.address)
        t = TokenAsset.objects.get(wallet=self,contract_address=contract_address)
        t.balance=balance
        t.save()

    def update_wallet(self):
        tokens =TokenAsset.objects.filter(wallet=self)
        for t in tokens:
            self.update_balance_of_contract(t.contract_address)


def create_wallet(password):
    address, account_encrypt = Web3Provider.create_eth_account(password)
    encrypted = json.dumps(account_encrypt)
    c = CryptoWallet(address=address, encrypted_private_key=encrypted, eth_balance=0)
    c.save()
    return c


def create_wallet_with_initial_10_eth(password):
    address, account_encrypt = Web3Provider.create_eth_account(password)
    encrypted = json.dumps(account_encrypt)
    c = CryptoWallet(address=address, encrypted_private_key=encrypted, eth_balance=0)
    c.save()
    result = get_eth_provider().get_credit(c.address, 10)
    c.get_balance()
    return c


class TokenAsset(models.Model):
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    contract_address = models.CharField(max_length=500)
    symbol = models.CharField(max_length=8)
    balance = models.BigIntegerField()

    def update_balance(self):
        eth_p = get_eth_provider()
        result = eth_p.get_project(self.contract_address).get_balance(self.wallet.address)
        return result
