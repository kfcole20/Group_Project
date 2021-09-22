from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register',views.register),
    path('main', views.main),
    path('login', views.login),
    path('logout', views.logout),
    path('details/<str:place_id>', views.bizdetails),
    path('search', views.search),
    path('favorite/<str:place_id>', views.favorite),
]