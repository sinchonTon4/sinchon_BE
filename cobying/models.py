from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from community.models import *

class Cobying(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)  # 제목
    description = models.TextField()  # 공구설명
    img = models.ImageField(blank=True, upload_to='cobying_images/')
    tag = models.ForeignKey(HashTag, on_delete=models.CASCADE)  # 해시태그 공동구매
    price = models.IntegerField(blank=True)
    product_name = models.TextField(max_length=50)
    link = models.TextField(null=True)
    people_num=  models.IntegerField(default=0)

    CATEGORY_CHOICES = [
        ('food', '식료품'),
        ('food', '생필품'),
    ]
    product_category = models.CharField(choices=CATEGORY_CHOICES, blank=True, null=True, max_length=50)

    def __str__(self):
        return self.product_category