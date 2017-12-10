import django.utils 

from django import forms
from django.db import models
from django.contrib.auth.models import User

class IngredientCategory(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    name = models.CharField(max_length=30)

class Ingredient(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    name = models.CharField(max_length=127)
    category = models.ForeignKey(IngredientCategory)
    
class DishType(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    name = models.CharField(max_length=30)    

class Receipt(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    sodium = models.IntegerField(default=0)
    dish_type = models.ManyToManyField(DishType)
    photo_url = models.TextField()
    instructions = models.TextField()

class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    contact_email = forms.EmailField()
    subject = forms.CharField(max_length=255)
#    botcheck = forms.CharField(max_length=5)
    message = forms.CharField()

