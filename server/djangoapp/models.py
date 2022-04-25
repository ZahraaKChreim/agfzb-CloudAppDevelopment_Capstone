from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=200)

    def __str__(self):
        return self.name + ': ' + self.description


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'Suv'
    WAGON = 'Wagon'
    TYPE_CHOICES = [ 
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(null=False, max_length=30)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    year = models.DateField(default=now)

    def __str__(self):
        return self.name + ', ' + self.type + ', ' + self.year



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
