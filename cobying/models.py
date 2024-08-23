from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from community.models import *

class Cobying(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50) #제목
    description = models.TextField() #공구설명
    img = models.ImageField(blank=True, upload_to='community_images/')
    tags = models.ForeignKey(HashTag, on_delete=models.CASCADE) #해시태그 공동구매..?
    price = models.IntegerField(blank=True)
    product_name = models.TextField(max_length=50)
    link = models.TextField(null=True)
    people_num = models.IntegerField()
    count = models.IntegerField(default=0)

    CATEGORY_CHOICES = [
        ('fooditem', '식료품'),
        ('lifeitem', '생필품'),
    ]
    product_category = models.CharField(choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.product_category
    
    
class HashTag(models.Model):
    hashtag = models.TextField(unique=True)
    communities = models.ManyToManyField('Community', related_name='tagged_hashtags')

    def __str__(self):
        return self.hashtag