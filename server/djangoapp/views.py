from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {'message': ''}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            context['message'] = "Invalid username or password."
    return redirect(reverse('djangoapp:index') + '?message=' + context['message'])

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {'message': request.GET.get('message')}
    if request.method == "GET":
        dealerships = get_dealers_from_cf("https://5e273dc5.us-south.apigw.appdomain.cloud/api/dealership")
        context['dealerships'] = dealerships
#        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context)
#        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealers = get_dealers_from_cf("https://5e273dc5.us-south.apigw.appdomain.cloud/api/dealership?dealerId=" + str(dealer_id))
        context['dealer'] = dealers.pop()
        reviews = get_dealer_reviews_from_cf("https://5e273dc5.us-south.apigw.appdomain.cloud/api/review?dealerId=" + str(dealer_id))
        context['reviews'] = reviews
#        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/dealer_details.html', context)
        #return HttpResponse(reviews)

# Create a `add_review` view to submit a review
#@csrf_exempt
def add_review(request, dealer_id):
    response = HttpResponse()
    if request.method == "POST" and request.user.is_authenticated:
        review = dict()
        review['time'] = datetime.utcnow().isoformat()
        review['dealership'] = dealer_id
        review['name'] = request.user.first_name + ' ' + request.user.last_name
        review['review'] = request.POST.get('review')
        review['purchase'] = bool(request.POST.get('purchase'))
        if review['purchase']:
            review['purchase_date'] = request.POST.get('purchase_date')
            car = CarModel.objects.get(id=request.POST.get('car'))
            review['car_make'] = car.car_make.name
            review['car_model'] = car.name
            review['car_year'] = car.car_year.strftime("%Y")
        json_payload = dict()
        json_payload['review'] = review
        response_data = post_request("https://5e273dc5.us-south.apigw.appdomain.cloud/api/review", json_payload)
        response = redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        context = {}
        dealers = get_dealers_from_cf("https://5e273dc5.us-south.apigw.appdomain.cloud/api/dealership?dealerId=" + str(dealer_id))
        context['dealer'] = dealers.pop()
        cars = CarModel.objects.all()
        context['cars'] = cars
        response = render(request, 'djangoapp/add_review.html', context)
    return response
