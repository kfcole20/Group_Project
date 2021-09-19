from django.db import models
import re, bcrypt
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField


# Create your models here.

class UserValidation(models.Manager):
    #Validations for registration page
    def register(self, post):
        email_ver = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post['first_name']) < 2 or len(post['last_name']) < 2:
            errors['name'] = 'Name entry not valid!'
        if not email_ver.match(post['email']):
            errors['email'] = 'Email format incorrect!'
        if len(post['pw']) == 0:
            errors['pw'] = 'Password needed to continue!'
        elif post['pw'] != post['confirm_pw']:
            errors['password'] = 'Passwords must match!'
        return errors

    #Validations for logging in
    def verify(self, post):
        errors = {}
        user_logged = User.objects.filter(email=post['email'])
        if len(post['email']) == 0:
            errors['email'] = 'Enter an email please!'
        elif len(user_logged) == 0:
            errors['no_user'] = 'No user with that email'
        if len(post['pw']) == 0:
            errors['pw'] = 'Password needed to continue!'
        elif not bcrypt.checkpw(post['pw'].encode(), user_logged[0].pw.encode()):
            errors['incorrect'] = 'Password/Email combination incorrect'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserValidation()

