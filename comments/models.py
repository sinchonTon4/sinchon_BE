from django.db import models
from auths.models import User
from community.models import Community

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='comments', null=True)
    description = models.TextField()
    like = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description