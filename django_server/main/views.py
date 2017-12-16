import logging
import json
import random
import sys
import string
import time
from threading import Thread
import traceback
import django.utils

from django.db import connection
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.views.generic.base import TemplateView
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Context
from django.core.mail import EmailMessage

from main.models import EmailForm, Receipt, IngredientCategory, Ingredient, DishType

OwnerEmail = 'denis_der@mail.ru'
NoReplyEmail = 'plan4nutrition@gmail.com'
logger = logging.getLogger('django')

no_photo = [
"https://assets.epicurious.com/photos/5a0ddb046e013d11dde39630/6:4/w_322,h_314,c_limit/no-recipe-card-green-15112017.jpg",
"https://assets.epicurious.com/photos/5a0ddb06f110de5830af9a10/6:4/w_322,h_314,c_limit/no-recipe-card-red-15112017.jpg",
"https://assets.epicurious.com/photos/5a0ddb14c8636449b01bb813/6:4/w_322,h_314,c_limit/no-recipe-card-blue-15112017.jpg"
]

#-------------------------------------------------------
#    PAGES
#-------------------------------------------------------

def main_menu(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('front_page'))
    return render(request, 'menu/index.html', {})


def front_page(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('front_page/index.html', c, {})

def login_view(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8');
            message = json.loads(body_unicode)

            username = message['username']
            password = message['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'success.html', {}) 
                else:
                    error = "You've been banned from this server."
            else:
                error = 'Incorrect login or password.'

            context = {
                'error': error,
            } 

            return render(request, 'failure.html', context)
        except:
            return render(request, 'failure.html', context)

    else:
        context = {
            'error': "Incorrect request",
        }
        return render(request, 'failure.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/index/')

def prelogin(request):
    c = {}
    c.update(csrf(request))
    context = Context({})
    return render_to_response('login.html', c, context)

def preregistration(request):
    c = {}
    c.update(csrf(request))
    context = Context({
    })
    return render_to_response('registration.html', c, context)

def registration_view(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8');
            message = json.loads(body_unicode)

            username = message['username']
            password = message['password']
            email = message['email']
            first_name = message['first_name']
            last_name = message['last_name']
            User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user = authenticate(username=username, password=password)
            login(request, user)
            
            
            sbg = "Welcome to Nutrition Plan!"
            tmp = django.template.loader.get_template('emails/Welcome.html')
            text = tmp.render({'name': first_name.capitalize()})  
            #print(text)
            thread = Thread(target = send_mail, args = (sbg, text, [email], True, ))
            thread.start()            

            return render(request, 'success.html', {})
        except:
            context = {
                'error': "Failed. Please, try changing username.",
            }
            return render(request, 'failure.html', context)

    else:
        context = {
            'error': "Incorrect request",
        }
        return render(request, 'failure.html', context)
    
def share_ideas(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8');
        #logger.error(json.loads(body_unicode))
        form = EmailForm(json.loads(body_unicode))
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['contact_email']
            subject = form.cleaned_data['subject']
            #botcheck = form.cleaned_data['botcheck'].lower()
            message = form.cleaned_data['message']
            if True: #botcheck == 'yes':
                fullsubject = "[P4N | Written via form on site] {}".format(subject)
                fullmessage = "From: {}, {} | {}\n\n{}".format(firstname, lastname, email, message)  
                if send_mail(fullsubject, fullmessage, [OwnerEmail], False):
                    return render(request, 'success.html', {})
                return render(request, 'failure.html', {})
                
        else:
            return render(request, 'failure.html', {})
    else:
        return render(request, 'failure.html', {})    
    
def detail(request):
    try:
        obj = Receipt.objects.get(id=int(QueryDict(request.GET.urlencode())['id']))
        types = []
        for i in obj.dish_type.all():
            types += [i.name]
        ingredients = []
        for i in obj.ingredients.all():
            ingredients += [i.name]        
        return HttpResponse('''
Recipe: {}
Ingredients: {}
Calories: {}
Proteins: {}
Fat: {}
Sodium: {}
Type: {}
Instructions: {}
'''.format(obj.name, 
           ", ".join(ingredients),
           obj.calories, obj.protein, obj.fat, obj.sodium, 
           ", ".join(types),
           obj.instructions.replace("/n", "\n")))
    except:
        return render(request, 'failure.html', {'error': "Can't find recipe"}) 
    
    
def search(request):
    #print("\n\n\n\n\n\n\n\n\n\n", request.GET.urlencode())
    
    search_req = 'r.name like "%{}%"'
    dishtype_req = 'd.name = "{}"'
    dishtype_full = 'HAVING sum( case when {} then 1 end) >= {}'
    with_photo_req = 'r.photo_url not like "%None%"'
    protein_min_req = 'r.protein >= {}'
    protein_max_req = 'r.protein <= {}'
    fat_min_req = 'r.fat >= {}'
    fat_max_req = 'r.fat <= {}'
    cal_min_req = 'r.calories >= {}'
    cal_min_req = 'r.calories >= {}'
    
    query = QueryDict(request.GET.urlencode())
    dish_types = request.GET.getlist('dishtype[]')
    requests = []
    if 'search' in query and query['search'] != '':
        requests += ["(" + " OR ".join(search_req.format(i) for i in query['search'].split()) + ")"]
    if 'withphoto' in query:
        requests += [with_photo_req]
    if 'proteinmin' in query and query['proteinmin'] != '':
        requests += [protein_min_req.format(query['proteinmin'])]    
    if 'proteinmax' in query and query['proteinmax'] != '':
        requests += [protein_max_req.format(query['proteinmax'])]    
    if 'fatmin' in query and query['fatmin'] != '':
        requests += [fat_min_req.format(query['fatmin'])]    
    if 'fatmax' in query and query['fatmax'] != '':
        requests += [fat_max_req.format(query['fatmax'])]    
    if 'calmin' in query and query['calmin'] != '':
        requests += [cal_min_req.format(query['calmin'])]    
    if 'calmax' in query and query['calmax'] != '':
        requests += [cal_min_req.format(query['calmax'])] 
        
    if len(dish_types) != 0:
        dishtype_ready = dishtype_full.format(' OR '.join(dishtype_req.format(i) for i in dish_types), len(dish_types))
    else:
        dishtype_ready = ""
        
    if len(requests) == 0 and dishtype_ready == "": 
        return HttpResponse()
    if len(requests) == 0:
        requests_ready = ""
    else:
        requests_ready = "WHERE " + " AND ".join(requests)
    
    print('''
SELECT r.id, r.name, r.photo_url FROM main_receipt r
JOIN
 main_receipt_dish_type rd on r.id = rd.receipt_id 
JOIN
 main_dishtype d on rd.dishtype_id = d.id
{}
GROUP BY r.id, r.name, r.photo_url
{}
limit 60
'''.format(requests_ready, dishtype_ready))
    
    results = []
    for i in Receipt.objects.raw('''
SELECT r.id, r.name, r.photo_url FROM main_receipt r
JOIN
 main_receipt_dish_type rd on r.id = rd.receipt_id 
JOIN
 main_dishtype d on rd.dishtype_id = d.id
{}
GROUP BY r.id, r.name, r.photo_url
{}
limit 60
'''.format(requests_ready, dishtype_ready)):
        results += [{
            'link': reverse('detail') + "?id={}".format(i.id),
            'title': i.name,
            'flex': 4,
        }]
        if "None" in i.photo_url or "http" not in i.photo_url:
            results[-1]['img'] = random.choice(no_photo)
        else:
            results[-1]['img'] = i.photo_url
    return HttpResponse(json.dumps(results))

def add_recipe(request):
    #print("\n\n\n\n\n\n\n\n\n\n", request.GET.urlencode())
    
    query = QueryDict(request.GET.urlencode())
    dish_types = request.GET.getlist('dishtype[]')
    insert_info = []
    if 'name' not in query:
        return HttpResponse()
    
    insert_info += ["'{}'".format(query['name'])]
    insert_info += [
        str(int(query['protein'])) if 'protein' in query else "0",
        str(int(query['fat'])) if 'fat' in query else "0",
        str(int(query['cal'])) if 'cal' in query else "0",
        "0", "'None'",
        "'{}'".format(query['instructions']) if 'instructions' in query else "''"
    ]
    
    print('''
INSERT INTO main_receipt (name, protein, fat, calories, sodium, photo_url, instructions)
VALUES ({})
'''.format(", ".join(insert_info)))
    
    results = []
    connection.cursor().execute('''
INSERT INTO main_receipt (name, protein, fat, calories, sodium, photo_url, instructions)
VALUES ({})
'''.format(", ".join(insert_info)))
    
    i = Receipt.objects.get(name=query['name'])
    results += [{
        'link': reverse('detail') + "?id={}".format(i.id),
        'title': i.name,
        'flex': 4,
    }]
    if "None" in i.photo_url or "http" not in i.photo_url:
        results[-1]['img'] = random.choice(no_photo)
    else:
        results[-1]['img'] = i.photo_url
        
    if "ingredient[]" in query:
        for j in request.GET.getlist('ingredient[]'):
            ing = Ingredient.objects.get(name=j)
            connection.cursor().execute('''
INSERT INTO main_receipt_ingredients (receipt_id, ingredient_id)
VALUES ({}, {})
        '''.format(i.id, ing.id))            
            
    return HttpResponse(json.dumps(results))


#-------------------------------------------------------
#    EXTRA
#-------------------------------------------------------
                                                              
def send_mail(subject, text, recipients, html):
    try:
        #logger.error("Trying to send")

        email = EmailMessage(subject, text, NoReplyEmail, recipients)
        if html:
            email.content_subtype = "html"
        email.send()
        #logger.error("Message was sent")
        return 1
    except:
        return 0



