from django.db import models
from django.conf import settings
from community.models import HashTag

class Cobying(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)  # 제목
    description = models.TextField()  # 공구설명
    img = models.ImageField(blank=True, upload_to='cobying_images/')
    tag = models.ForeignKey(HashTag, on_delete=models.CASCADE)  # 해시태그 공동구매
    price = models.IntegerField(blank=True)
    product_name = models.CharField(max_length=50)
    link = models.TextField(null=True)
    people_num = models.IntegerField()

    FOOD = 1
    HOUSEHOLD = 2
    CATEGORY_CHOICES = [
        (FOOD, '식료품'),
        (HOUSEHOLD, '생필품'),
    ]
    product_category = models.IntegerField(choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.title 