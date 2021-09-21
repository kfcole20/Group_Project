from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

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
    context={
        'user':User.objects.get(id=request.session['id'])
    }
    return render(request, 'main.html', context)

def edit(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'edit.html', context)