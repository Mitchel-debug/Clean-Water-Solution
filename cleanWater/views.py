import email
from locale import currency
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import requests
from urllib3 import HTTPResponse
from Waterways.mixins import Directions
import cleanWater
from django.http import HttpResponseRedirect, JsonResponse
import stripe
from humanfriendly import format_timespan
from .models import Articles, User, UserProfile

stripe.api_key = "sk_test_51LyJ17BSE8CSa3qNLumX2XXGcoidGdc3sypq7xVE8sLhD2e8Oa7NAweBoNhDQdyVYHzdTWdDjmsvzuhXUhurgtvV008Np5GhjP" 

def index(request):
    list = (0, 1, 2)
    artricle = Articles.objects.all().order_by("-id")[:3]
    return render(request, "cleanWater/index.html", {
        "List": list,
        "art4": artricle
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


def profile(request):
    if request.method == "POST":
        usernames = request.POST["username"]
        addresss = request.POST.get("address")
        towns = request.POST["town"]
        countys = request.POST["county"]
        post_codes = request.POST["post_code"]
        countrys = request.POST["country"]
        longitude = request.POST["longitude"]
        latitude = request.POST["latitude"]
        had = True
        is_private = request.POST.get('is_private', False)
        curentU = User.objects.get(username = usernames)

        userCreated = UserProfile(
                user = curentU,
                address = addresss,
                town=towns,
                county=countys,
                post_code=post_codes,
                country=countrys,
                longitude=longitude,
                latitude=latitude,
                has_profile = True
            )
        userCreated.save()
        return HttpResponseRedirect(reverse(index))
    profileData = UserProfile.objects.all()
    return render(request, "cleanWater/profile.html", {
        "data": profileData,
        "google_api_key": settings.GOOGLE_API_KEY,
        "base_country": settings.BASE_COUNTRY,
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
    
def route(request):

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY}
	return render(request, 'cleanWater/route.html', context)


'''
Basic view for displaying a map 
'''
def map(request):

	lat_a = request.GET.get("lat_a", None)
	long_a = request.GET.get("long_a", None)
	lat_b = request.GET.get("lat_b", None)
	long_b = request.GET.get("long_b", None)
	lat_c = request.GET.get("lat_c", None)
	long_c = request.GET.get("long_c", None)
	lat_d = request.GET.get("lat_d", None)
	long_d = request.GET.get("long_d", None)


	#only call API if all 4 addresses are added
	if lat_a and lat_b and lat_c and lat_d:
		directions = Directions(
			lat_a= lat_a,
			long_a=long_a,
			lat_b = lat_b,
			long_b=long_b,
			lat_c= lat_c,
			long_c=long_c,
			lat_d = lat_d,
			long_d=long_d
			)
	else:
		return redirect(reverse('route'))

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"lat_c": lat_c,
	"long_c": long_c,
	"lat_d": lat_d,
	"long_d": long_d,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'cleanWater/map.html', context)
