from main.models import Receipt
import ast

def run():
    for i in Receipt.objects.all():
        nutr = i.nutrition
        if "nan" not in nutr:
            try:
                cal, p, f, sod = list(map(lambda x: int(float(x)), ast.literal_eval(nutr)))
                i.calories = cal
                i.protein = p
                i.fat = f
                i.sodium = sod
                i.save()
            except:
                print(nutr)