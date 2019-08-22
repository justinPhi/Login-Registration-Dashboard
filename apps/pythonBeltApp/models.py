import bcrypt
from django.db import models
import re

emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class MyValidator(models.Manager):
    def valReg(self, userData):
        errors = {}

        #Firstname validation
        if len(userData["firstName"]) < 4:
            errors["nameLeng"] = "Name  must be at least 4 characters long"

        #Lastname validation 
        if len(userData["lastName"]) < 4:
            errors["lastNameLeng"] = "Lastname must be at least 4 characters long"

        #Password validation
        if len(userData["password"]) < 8:
            errors["passLeng"] = "Password must be at least 8 characters"
        if not userData["password"] == userData["passwordConfirm"]:
            errors["passConfirm"] = "Passwords need to match"

        #Email validation for if already in DB
        if User.objects.filter(email = userData["email"]):
            errors["emailExists"] = "Someone with this username has already registered"
        elif not emailRegex.match(userData["email"]):
            errors["emailExists"] = "Not a valid email address"
            

        return errors

    def validateLogin(self, userData):
        errors = {}

        #Check valid email
        try:
            user = User.objects.get(email = userData["email"])
        except:
            errors["email"] = f"No email address matching {userData['email']}"
            return errors

        #Check matching password
        if not bcrypt.checkpw(userData["password"].encode(), user.password.encode()):
            errors["password"] = "Password does not match email"
        
        return errors

class User(models.Model):
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    
    objects = MyValidator()

