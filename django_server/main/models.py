import django.utils 

from django import forms
from django.db import models
from django.contrib.auth.models import User

class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    contact_email = forms.EmailField()
    subject = forms.CharField(max_length=255)
#    botcheck = forms.CharField(max_length=5)
    message = forms.CharField()

