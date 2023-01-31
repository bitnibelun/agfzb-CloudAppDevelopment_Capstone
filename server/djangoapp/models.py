from django.db import models
from django.utils.timezone import now


# Create your models here.
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    HONDA = 'Honda'
    GMC = 'GMC'
    FORD = 'Ford'
    SUBARU = 'Subaru'
    BMW = 'BMW'
    TOYOTA = 'Toyota'
    MAKES = [(HONDA, 'Honda'), (GMC,'GMC'), (FORD, 'Ford'), (SUBARU, 'Subaru'), (BMW, 'BMW'), (TOYOTA, 'Toyota')]
    name = models.CharField(null = False, max_length = 35, choices = MAKES, default = HONDA)
    description = models.CharField(null = True, max_length = 300)

    def __str__(self):
        return str(self.name)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null = True, on_delete = models.CASCADE)
    dealer_id = models.IntegerField(null = True)
    name = models.CharField(null = False, max_length = 25)

    SEDAN = 'Sedan'
    PICK_UP = 'Pick-Up'
    VAN = 'Van'
    SUV = 'Suv'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    SPORTS_CAR = 'Sport'
    OTHER = 'Other_Car'
    TYPES = [(SEDAN, 'Sedan'), (PICK_UP, 'Pick-Up Truck'), (VAN, 'Van'),
    (SUV, 'Suv'), (WAGON, 'Wagon'), (COUPE, 'Coupe'),
    (SPORTS_CAR, 'Sports Car'), (OTHER, 'Other Car')]
    car_type = models.CharField(null = False, max_length = 20, choices = TYPES, default = SEDAN)
    year = models.DateField(null = False)

    def __str__(self):
        return str(self.year) + ", " + self.name + ", " + self.car_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
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


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, r_id, dealership, name, purchase, review, purchase_date = None,
                 car_make = None, car_model = None, car_year = None, sentiment=None):
        self.dealership = dealership
        self.name = name  
        self.purchase = purchase  
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year   
        self.sentiment = sentiment
        self.id = r_id 

    def __str__(self):
        return "Name: " + self.name +", Review: " + self.review
