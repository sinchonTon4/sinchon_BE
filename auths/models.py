from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# AbstractUser에 username(아이디), password(비밀번호) 포함(자동생성)
class User(AbstractUser):
    phonenum = models.IntegerField(blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    univname = models.CharField(max_length=20, null=True)
    
    def __str__ (self):
        return self.username
    
