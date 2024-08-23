from django.db import models

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=20)
    ingredient_price = models.IntegerField()