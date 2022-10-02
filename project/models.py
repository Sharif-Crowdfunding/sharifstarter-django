from django.db import models

from user.models import User


# Create your models here.
class ProjectBasicInfo(models.Model):
    website = models.CharField('لینک وبسایت', max_length=400)
    telegram_id = models.CharField('آیدی تلگرام ', max_length=400)
    token_info = models.CharField('توکن پروژه', max_length=400)
    details = models.CharField('توضیحات پروژه', max_length=400)
    github_id = models.CharField(' آیدی گیتهاب', max_length=400)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    basicInfo = models.OneToOneField(ProjectBasicInfo, on_delete=models.CASCADE)
    name = models.CharField('نام پروژه', max_length=400)
    contract_address = models.CharField('آدرس کانترکت پروژه', max_length=400)
    creator_address = models.CharField('آدرس کیف‌پول سازنده', max_length=400)
    image = models.CharField('عکس', max_length=400)
