from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt, os
from .models import User
from .api import *
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors=User.objects.register(request.POST)
    if request.method!= 'POST':
        return redirect('/')
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    new_user= User.objects.create(
        first_name= request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['id']= new_user.id
    return redirect('/main')

def login(request):
    errors= User.objects.verify(request.POST)
    if request.method!= 'POST':
        return redirect('/')
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user_logged=User.objects.filter(email=request.POST['email'])[0]
    request.session['id'] = user_logged.id
    return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/')    

def main(request):
    if 'id' not in request.session:
        return redirect('/')
    context={
        'user':User.objects.get(id=request.session['id'])
    }
    return render(request, 'main.html', context)

def bizdetails(request):
    if 'id' not in request.session:
        return redirect('/')
    context={
        # add business object and loop through until business in session is found
        'user': User.objects.get(id=request.session['id'])
    }
    return render (request, 'details.html', context)

def search(request):
    client= GoogleMapsClient()
    locations_list=[]
    for location in client.search(location=request.POST['search_space'])['results']:
        locations_list.append(client.detail(place_id=location['place_id'])['result'])
    context={
        'locations':locations_list,
        'user':User.objects.get(id=request.session['id'])
    }
    return render(request, 'search.html', context)
