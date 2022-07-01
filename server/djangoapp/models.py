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


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
        

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
#        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.name