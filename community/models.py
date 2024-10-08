from django.db import models
from auths.models import User
from django.conf import settings

class Community(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='community_images/')
    like = models.IntegerField(default=0)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField('HashTag', related_name='tagged_communities', blank=True)
    
    CATEGORY_CHOICES = [
        ('food', 'food'),
        ('lifestyle', 'lifestyle'),
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30, default='food')

    def __str__(self):
        return self.title
    
class HashTag(models.Model):
    hashtag = models.TextField(unique=True)
    communities = models.ManyToManyField('Community', related_name='tagged_hashtags')

    def __str__(self):
        return self.hashtag