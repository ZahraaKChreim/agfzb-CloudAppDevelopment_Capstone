from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview, ReviewPost
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def simple(request):
    return render(request, 'static.html')


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            #return redirect('djangoapp:index')
        # else:
        #     # If not, return to login page again
        #     return render(request, 'onlinecourse/user_login.html', context)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://8f86aac1.eu-gb.apigw.appdomain.cloud/dealership/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = f"https://8f86aac1.eu-gb.apigw.appdomain.cloud/review_of_dealership/review_of_dealership?id={id}"
        reviews = get_dealer_reviews_from_cf(dealer_url, dealer_Id=id)
        context["id"] = id
        if not reviews:
            context["reviews"] = 'No reviews for this dealer, or dealer not found'
        else:
            context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

# def add_review(request, id):
#     if request.user.is_authenticated:
#         new_review = dict()
#         new_review["id"]= 1115,
#         new_review["name"]= "Zahraa ch",
#         new_review["dealership"]= 1,
#         new_review["review"]= "Not bad",
#         new_review["purchase"]= False,
#         new_review["another"]= "field",
#         new_review["purchase_date"]= "04/27/2022",
#         new_review["car_make"]= "BMW",
#         new_review["car_model"]= "Range",
#         new_review["car_year"]= 2021

#         review_payload = {}
#         review_payload = new_review

#         review_payload_json = json.dumps(review_payload)
#         print("review_payload_json",review_payload_json)

#         review_post_url = "https://8f86aac1.eu-gb.apigw.appdomain.cloud/review_of_dealership/review/review"
#         parameters = {"dealership":id}
#         post_response = post_request(review_post_url, review_payload_json, **parameters)
#         return HttpResponse(post_response)
#     else:
#         return HttpResponse("User unauthorized")

# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    dealer_url = "https://8f86aac1.eu-gb.apigw.appdomain.cloud/dealership/dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, dealerId=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.filter(id=id)
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            # payload["time"] = datetime.utcnow().isoformat()
            # payload["name"] = username
            # payload["dealership"] = id
            # payload["id"] = id
            # payload["review"] = request.POST["content"]
            # payload["purchase"] = False
            # if "purchasecheck" in request.POST:
            #     if request.POST["purchasecheck"] == 'on':
            #         payload["purchase"] = True
            # payload["purchase_date"] = request.POST["purchasedate"]
            # payload["car_make"] = car.car_make
            # payload["car_model"] = car.name
            # payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            review_content =  dict()
            review_content["id"] = id
            review_content["name"] = username
            review_content["dealership"] = id
            review_content["review"] = request.POST["content"]
            review_content["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review_content["purchase"] = True
            review_content["purchase_date"] =  request.POST["purchasedate"]
            # review_content["car_make"] = car.car_make
            # review_content["car_model"] = car.name
            # review_content["car_year"] = int(car.year.strftime("%Y"))
            
            review_content["car_make"] = getattr(car, 'car_make')
            review_content["car_model"] = getattr(car, 'name')
            review_content["car_year"] = int((getattr(car, 'year')).strftime("%Y"))

            from djangorestframework.serializers import serialize
            data = serialize('json', review_content)
            new_payload["review"] = review_content

            review_post_url = "https://8f86aac1.eu-gb.apigw.appdomain.cloud/review/review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)

