from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["dealer_id", 'year', 'make', 'car_type', 'name']
    list_filter = ['name', 'make', 'dealer_id', 'car_type']
    search_fields = ['make', 'name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)