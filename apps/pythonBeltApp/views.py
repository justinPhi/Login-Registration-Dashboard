from django.shortcuts import render, redirect
import bcrypt
from .models import User
from django.contrib import messages


def index(request):
    return render(request, "pythonBeltApp/logReg.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.valReg(request.POST)
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/")

        newUser = User(
                firstName = request.POST["firstName"],
                lastName = request.POST["lastName"],
                email = request.POST["email"],
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
                )

        newUser.save()
        addedUser = User.objects.get(email = newUser.email)
        request.session['user'] = addedUser.id
        return redirect("/dashboard")
            
    

def login(request):
    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/index")
        loginuser = User.objects.get(email=request.POST["email"])
        request.session['user'] = loginuser.id
    return redirect("/dashboard")

def displayDashboard(request):
    if 'user' not in request.session:
        messages.error(request, "For some reason you are trying to view a page that you are not allowed to view")
        return redirect("/")
    if request.method == "GET":
        context = {
                "users" : User.objects.filter(id = request.session["user"]),
                }

    return render(request, "pythonBeltApp/dashboard.html", context)



# Create your views here.
