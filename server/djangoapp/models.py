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


# <HINT> Create a plain Python class `DealerReview` to hold review data