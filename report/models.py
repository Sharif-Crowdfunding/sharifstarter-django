from django.db import models


# Create your models here.
class ReportExam(models.Model):
    title = models.CharField(max_length=200, unique=False, verbose_name="تیتر گزارش")
    exam_num = models.IntegerField()
