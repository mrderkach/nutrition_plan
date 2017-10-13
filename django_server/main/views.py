import logging
import json
import random
import sys
import string
import time
import traceback
import django.utils

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Context
from django.core.mail import EmailMessage

from main.models import EmailForm

OwnerEmail = 'denis_der@mail.ru'
NoReplyEmail = 'plan4nutrition@gmail.com'
logger = logging.getLogger('django')

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

#-------------------------------------------------------
#    EXTRA
#-------------------------------------------------------
                                                              
def send_mail(request):
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
                try:
                    #logger.error("Trying to send")
                    fullsubject = "[P4N | Written via form on site] {}".format(subject)
                    fullmessage = "From: {}, {} | {}\n\n{}".format(firstname, lastname, email, message)
                    email = EmailMessage(fullsubject, fullmessage, NoReplyEmail, [OwnerEmail])
                    #email.content_subtype = "html"
                    email.send()
                    #logger.error("Message was sent")
                    return render(request, 'success.html', {})
                except:
                    return render(request, 'failure.html', {})
        else:
            return render(request, 'failure.html', {})
    else:
        return render(request, 'failure.html', {})



