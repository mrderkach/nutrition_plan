from django.contrib import admin
from .models import Receipt, IngredientCategory, Ingredient, DishType

admin.site.register(Receipt)
admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
admin.site.register(DishType)
