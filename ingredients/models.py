from django.db import models

class Ingredient(models.Model):
    necessary_name = models.CharField(max_length=20)
    necessary_price = models.IntegerField()