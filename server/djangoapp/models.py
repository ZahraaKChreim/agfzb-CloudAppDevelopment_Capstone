# from django.db import models
# from django.utils.timezone import now
# from django.core import serializers 
# import uuid
# import json

# # Create your models here.

# class CarMake(models.Model):
#     name = models.CharField(null=False, max_length=30)
#     description = models.CharField(null=False, max_length=200)

#     def __str__(self):
#         return self.name + ': ' + self.description


# class CarModel(models.Model):
#     SEDAN = 'Sedan'
#     SUV = 'Suv'
#     WAGON = 'Wagon'
#     TYPE_CHOICES = [ 
#         (SEDAN, 'Sedan'),
#         (SUV, 'Suv'),
#         (WAGON, 'Wagon')
#     ]
#     car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
#     dealer_id = models.IntegerField(default=0)
#     name = models.CharField(null=False, max_length=30)
#     type = models.CharField(max_length=5, choices=TYPE_CHOICES)
#     year = models.DateField(default=now)

#     def __str__(self):
#         return self.name + ', ' + self.type + ', ' + self.year



# # <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer:

#     def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
#         # Dealer address
#         self.address = address
#         # Dealer city
#         self.city = city
#         # Dealer Full Name
#         self.full_name = full_name
#         # Dealer id
#         self.id = id
#         # Location lat
#         self.lat = lat
#         # Location long
#         self.long = long
#         # Dealer short name
#         self.short_name = short_name
#         # Dealer st
#         self.st = st
#         # Dealer state
#         self.state = state
#         # Dealer zip
#         self.zip = zip

#     def __str__(self):
#         return "Dealer name: " + self.full_name

# # <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview:

#     def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        
#         self.dealership = dealership
#         self.name = name
#         self.purchase = purchase
#         self.review = review
#         self.purchase_date = purchase_date
#         self.car_make = car_make
#         self.car_model = car_model
#         self.car_year = car_year
#         self.sentiment = sentiment
#         self.id = id

#     def __str__(self):
#         return "Dealer Review: " + self.review


############################################
############################################

from django.db import models
from django.utils.timezone import now
from django.core import serializers 
import uuid
import json


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, default='undefined')
    # - Name
    description = models.TextField(null=True)
    # - Description
    def __str__(self):
    # - __str__ method to print a car make object
        return self.name + ": " + self.description


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    name = models.CharField(null=False, max_length=40, default='undefined')
    # - Name
    dealer_id = models.CharField(null=False, max_length=40, default='undefined')        
    # - Dealer id, used to refer a dealer created in cloudant database
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    SPORTS = 'Sports'
    HATCHBACK = 'Hatchback'
    CONVERTIBLE = 'Convertible'
    MINIVAN = 'Minivan'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (SPORTS, 'Sports'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
        (MINIVAN, 'Minivan'),   
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=COUPE
    )
    # - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    year = models.DateField(null=False)
    # - Year (DateField)
    year = models.DateTimeField('date designed')
    def __str__(self):
        return self.type
    # - __str__ method to print a car make object


class CarDealer:


    def __init__(self, address, city, id, lat, long, st, state, zip, full_name, short_name):
        self.address = address
        self.city = city
        self.id = id
        self.lat = lat
        self.long = long
        self.st = st
        self.state = state
        self.zip = zip
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, id, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment):
        
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)

class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)