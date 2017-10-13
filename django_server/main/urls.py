from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    url(r'^login/', views.prelogin, name='prelog'),
    url(r'^checklog/$', views.login_view, name='checklog'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^regcheck/', views.registration_view, name='checkreg'),
    url(r'^registration/', views.preregistration, name='prereg'),
    url(r'^email/send/$', views.send_mail, name='send_email'),

    url(r'^index/', views.front_page, name='front_page'),
    url(r'^$', views.main_menu, name='menu'),
]
