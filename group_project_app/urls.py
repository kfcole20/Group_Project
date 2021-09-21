from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register',views.register),
    path('main', views.main),
    path('login', views.login),
    path('logout', views.logout),
    path('details', views.details),
    path('account', views.account),
]