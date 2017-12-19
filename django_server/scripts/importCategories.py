import ast
import csv
from main.models import IngredientCategory, Ingredient
from django_server.settings import BASE_DIR

def run():
    d = "/".join(BASE_DIR.split("/")[:-1]) + "/DB/"
    
    #with open(d + "categories.txt") as f:
        #reader = csv.reader(f)
        #i = 0
        #for row in reader:
            #if i != 0:
                #try:
                    #_, created = IngredientCategory.objects.get_or_create(
                        #id=int(row[0]),
                        #name=row[1],
                        #)
                #except:
                    #obj= IngredientCategory.objects.get(id=int(row[0]),)
                    #obj.name = row[1]
                    #obj.save()                     
            #i += 1
            
    with open(d + "ingr_by_categ.txt") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                try:
                    obj= Ingredient.objects.get(name=row[0])
                    obj.category = IngredientCategory.objects.get(id=int(row[1]))
                    obj.save() 
                except:
                    print(row[0])
            i += 1