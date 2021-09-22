from django.db import models
import re, bcrypt
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
        if len(post['password']) == 0:
            errors['password'] = 'Password needed to continue!'
        elif post['password'] != post['confirm_password']:
            errors['password'] = 'Passwords must match!'
        return errors

    #Validations for logging in
    def verify(self, post):
        errors = {}
        user_logged = User.objects.filter(email=post['email'])
        if len(post['email']) == False:
            errors['email'] = 'Enter an email please!'
        elif not user_logged:
            errors['no_user'] = 'No user with that email'
            return errors
        if len(post['password']) == 0:
            errors['password'] = 'Password needed to continue!'
        elif not bcrypt.checkpw(post['password'].encode(), user_logged[0].password.encode()):
            errors['incorrect'] = 'Password/Email combination incorrect'
        return errors

    def edit(self, post):
        errors = {}
        if len(post['first_name']) < 2:
            errors['first_name'] = "First Name must have at least 2 characters"
        if len(post['last_name']) < 2:
            errors['last_name'] = "Last Name must have at least 2 characters"
        if len(post['email']) < 2:
            errors['first_name'] = "Email must have at least 2 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserValidation()

class Business(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    favorited_by = models.ManyToManyField(User, related_name='favorite_bar')
    place_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)