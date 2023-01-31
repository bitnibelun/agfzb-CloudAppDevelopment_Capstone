from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealers_by_state_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        print('Here: about')
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        print('Here: contact')
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Wrong credentials. Try again!"
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        print('Here: contact')
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         print('Here: get_dealerships')
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/b611b81f-938e-43c4-965c-f566c4721a29/dealership-package/dealership-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships

        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/b611b81f-938e-43c4-965c-f566c4721a29/review-package/review-get"
        # Get dealer from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "reviews":  dealer_reviews, 
            "dealer_id": dealer_id
        }

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `get_dealer_by_state` view to render the dealerships from a particular state 
def get_dealers_by_state(request, state):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/b611b81f-938e-43c4-965c-f566c4721a29/dealership-package/dealership-get"
        # Get dealer from the URL
        dealerships = get_dealers_by_state_from_cf(url, state)
        context['dealerships'] = dealerships

        return render(request, 'djangoapp/index.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    
    if request.user.is_authenticated:
        if request.method == "GET":
            url = f"https://us-south.functions.appdomain.cloud/api/v1/web/b611b81f-938e-43c4-965c-f566c4721a29/review-package/review-get?dealerId={dealer_id}"
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id_from_cf(url, dealer_id = dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)

        if request.method == "POST":
            review = dict()
            from_form = request.POST
            car = CarModel.objects.get(pk = from_form["car"])

            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
            review["dealership"] = dealer_id
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["purchase"] = from_form.get("purchase_details")
            review["review"] = from_form["review_content"]

            if from_form.get("purchase_details"):
                review["purchase_date"] = datetime.strptime(from_form.get("purchase_date"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            url = "https://us-south.functions.appdomain.cloud/api/v1/web/b611b81f-938e-43c4-965c-f566c4721a29/review-package/review-post"
            json_payload = {"review": review}  
            result = post_request(url, json_payload, dealerId = dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id = dealer_id)

    else:
        return redirect("djangoapp/login")
