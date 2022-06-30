from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    CROSSOVER = 'crossover'
    CONVERTIBLE = 'convertible'
    COUPE = 'coupe'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (HATCHBACK, 'Hatchback'),
        (CROSSOVER, 'Crossover'),
        (CONVERTIBLE, 'Convertible'),
        (COUPE, 'Coupe')
    ]
    id = models.AutoField(primary_key=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer = models.IntegerField(default=0)
    car_type = models.CharField(
        null=False,
        max_length=15,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    car_year = models.DateField(null=True)
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type: " + self.car_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
