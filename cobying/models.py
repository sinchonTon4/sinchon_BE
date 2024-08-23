from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Community(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50) #제목
    description = models.TextField() #공구설명
    img = models.ImageField(blank=True, upload_to='community_images/')
    tag = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name='tag_interests') #수정필요 
    price = models.intfield
    product_name = models.TextField(max_length=50, blank=True, null=True)
    link = models.TextField(null=True)
    people_num=  models.IntegerField(blank=True, null=True, unique=True)
    product_category = models.IntegerField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.title