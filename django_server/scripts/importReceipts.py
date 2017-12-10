import ast
import csv
from main.models import Receipt, IngredientCategory, Ingredient, DishType
from django_server.settings import BASE_DIR

def run():
    d = "/".join(BASE_DIR.split("/")[:-1]) + "/DB/"
    
    with open(d + "db_ingredients_categories.csv") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                _, created = IngredientCategory.objects.get_or_create(
                    id=int(row[0]),
                    name=row[1],
                    )
            i += 1    
            
    with open(d + "db_ingredients.csv") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                _, created = Ingredient.objects.get_or_create(
                    id=int(row[0]),
                    name=row[1],
                    category=IngredientCategory.objects.get(id=1)
                    )
            i += 1  
            
    with open(d + "db_dishtype.csv") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                _, created = DishType.objects.get_or_create(
                    id=int(row[0]),
                    name=row[1],
                    )
            i += 1 
    
    with open(d + "db_receipts.csv") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            #print(row)
            try:
                if i != 0:
                    if len(row) < 7 or len(row[2]) == 0 or len(row[4]) == 0:
                        continue
                    
                    obj, created = Receipt.objects.get_or_create(
                        name=row[1],
                        nutrition=row[3],
                        photo_url=row[5],
                        instructions="".join(row[6:])
                        )
                    
                    if created:
                        for j in list(map(int, ast.literal_eval(row[2]))):
                            obj.ingredients.add(Ingredient.objects.get(id=j))
                            
                        for j in ast.literal_eval(row[4]):
                            obj.dish_type.add(DishType.objects.get(name=j))
                            
                        obj.save()
                i += 1
                if i % 200 == 0:
                    print(i)
            except:
                print(row)
    print(i)