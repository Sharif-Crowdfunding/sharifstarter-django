from enum import Enum

from django.db import models

from user.models import User
from utils.ethereum.blockchain import get_eth_provider


class DevelopmentStages(Enum):
    Inception = 0
    Elaboration = 1
    Deployment = 2
    Canceled = 3


# Create your models here.
class ProjectBasicInfo(models.Model):
    website = models.CharField('لینک وبسایت', max_length=400)
    telegram_id = models.CharField('آیدی تلگرام ', max_length=400)
    details = models.CharField('توضیحات پروژه', max_length=400)
    github_id = models.CharField(' آیدی گیتهاب', max_length=400)


class ProjectTokenInfo(models.Model):
    symbol = models.CharField('نماد', max_length=6)
    total_supply = models.BigIntegerField(default=0)
    development_stage = models.IntegerField(choices=[(tag, tag.value) for tag in DevelopmentStages],
                                            default=DevelopmentStages.Inception.value)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    basic_info = models.OneToOneField(ProjectBasicInfo, on_delete=models.CASCADE)
    token_info = models.OneToOneField(ProjectTokenInfo, on_delete=models.CASCADE)
    name = models.CharField('نام پروژه', max_length=400)
    contract_address = models.CharField('آدرس کانترکت پروژه', max_length=400)
    image = models.CharField('عکس', max_length=400)

    @property
    def is_deployed_on_chain(self):
        return len(self.contract_address) > 0

    def cancel(self):
        self.token_info.development_stage = DevelopmentStages.Canceled.value
        eth_p = get_eth_provider()
        p = eth_p.get_project(contract_address=self.contract_address)
        pk = eth_p.calc_private_key(self.user.wallet.encrypted_private_key, self.user.username)
        result = p.cancel(self.user.wallet.address, pk)
        print(result)
        self.token_info.save()

    def fund(self):
        self.token_info.development_stage = DevelopmentStages.Elaboration.value
        eth_p = get_eth_provider()
        p = eth_p.get_project(contract_address=self.contract_address)
        pk = eth_p.calc_private_key(self.user.wallet.encrypted_private_key, self.user.username)
        result = p.fund(self.user.wallet.address, pk)
        print(result)
        approve_result = p.approve_by_manager(eth_p.manager,eth_p.manager_pass)
        print(approve_result)
        self.token_info.save()

    def release(self):
        self.token_info.development_stage = DevelopmentStages.Deployment.value
        eth_p = get_eth_provider()
        p = eth_p.get_project(contract_address=self.contract_address)
        pk = eth_p.calc_private_key(self.user.wallet.encrypted_private_key, self.user.username)
        result = p.release(self.user.wallet.address, pk)
        print(result)
        self.token_info.save()

    # def get_auction(self):
    #     eth_p = get_eth_provider()
    #     p = eth_p.get_project(contract_address=self.contract_address)
    #     pk = eth_p.calc_private_key(self.user.wallet.encrypted_private_key, self.user.username)
    #     result = p.get_auctions(self.user.wallet.address, pk)
    #     print(result)
    #     return result