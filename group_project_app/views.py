from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt, os
from .models import User, Business
from .api import GoogleMapsClient
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
        'user':User.objects.get(id=request.session['id']),
        'favorites': Business.objects.all()
    }
    return render(request, 'main.html', context)

def bizdetails(request, place_id):
    if 'id' not in request.session:
        return redirect('/')
    client= GoogleMapsClient()
    location =client.detail(place_id=place_id)['result']
    location['place_id']=place_id
    context={
        # add business object and loop through until business in session is found
        'user': User.objects.get(id=request.session['id']),
        'location': location
    }
    return render (request, 'details.html', context)

def search(request):
    if 'id' not in request.session:
        return redirect('/')
    client= GoogleMapsClient()
    locations_list=[]
    for location in client.search(location=request.POST['search_space'])['results']:
        new_location=client.detail(place_id=location['place_id'])['result']
        new_location['place_id']=location['place_id']
        locations_list.append(new_location)
    context={
        'locations':locations_list,
        'user':User.objects.get(id=request.session['id'])
    }
    return render(request, 'search.html', context)

def favorite(request, place_id):
    this_user = User.objects.get(id=request.session['id'])
    client = GoogleMapsClient()
    location = client.detail(place_id=place_id)['result']
    this_location = Business.objects.create( 
        name=location['name'], 
        rating=location['rating'], 
        place_id=place_id, 
        location=location['formatted_address'] )
    this_location.favorited_by.add(this_user)
    return redirect('/main')

def account(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'edit.html', context)

def update(request):
    errors = User.objects.edit(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account')
    if request.method != 'POST' or 'id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=request.session['id'])
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        if len(request.POST['password'])==0:
            this_user.save()
            return redirect('/account')
        this_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        this_user.save()
        return redirect('/account')

def delete_fav(request, business_id):
    business_to_delete = Business.objects.get(id = business_id)
    business_to_delete.delete()
    return redirect('/main')