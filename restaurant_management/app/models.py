from django.db import models

class Category(models.Model):
    unique_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

class Item(models.Model):
    unique_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Ingredient(models.Model):
    unique_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Item_Ingredients(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)