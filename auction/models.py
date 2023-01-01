from django.db import models

from project.models import Project
from user.models import User


# Create your models here.
class Auction(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
