from django.contrib import admin
from .models import CarMake, CarModel, DealerReview


# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')


# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)