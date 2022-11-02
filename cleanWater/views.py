import email
from locale import currency
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from urllib3 import HTTPResponse
import cleanWater
from django.http import HttpResponseRedirect, JsonResponse
import stripe
from .models import Articles, User

stripe.api_key = "sk_test_51LyJ17BSE8CSa3qNLumX2XXGcoidGdc3sypq7xVE8sLhD2e8Oa7NAweBoNhDQdyVYHzdTWdDjmsvzuhXUhurgtvV008Np5GhjP" 

def index(request):
    list = (0, 1, 2)
    return render(request, "cleanWater/index.html", {
        "List": list
    })
    
def charge(request):
    amount=int(request.POST['amount'])
    if request.method == 'POST':
        print("Data: ", request.POST)
        
        customer = stripe.Customer.create(
            email = request.POST['email'],
            name = request.POST['nickname'],
            source = request.POST['stripeToken']
        )
        
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency="usd",
            description="Donation",
            
        )
        
    return HttpResponseRedirect(reverse("successMsg", args=[amount]))

def successMsg(request, args):
    amount = args
    return render(request, "cleanWater/success.html", {
        "amount": amount
    })
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cleanWater/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cleanWater/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cleanWater/register.html")
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cleanWater/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cleanWater/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def takeaction(request):
    return render(request, "cleanWater/takeAction.html")

def report(request):
    return render(request, "cleanWater/report.html")

def articles(request):
    article=Articles.objects.all()
    return render(request, "cleanWater/articles.html", {
        "Articles": article
    })
def about(request):
    return render(request, "cleanWater/about.html")

def showArticles(request, articles_id):
    art = Articles.objects.get(pk=articles_id)

    return render(request, "cleanWater/showArticle.html", {
        "art": art
    })