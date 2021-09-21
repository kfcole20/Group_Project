from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register',views.register),
    path('main', views.main),
    path('login', views.login),
    path('logout', views.logout),
<<<<<<< HEAD
    path('edit', views.edit),
=======
    path('details', views.bizdetails)
>>>>>>> 677770c9e78dc95011d30a8591694eb4aeeb99fe
]