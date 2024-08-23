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
    

    def __str__(self):
        return self.title
    
class HashTag(models.Model):
    hashtag = models.TextField(unique=True)

    def __str__(self):
        return self.hashtag