from django.contrib import admin
from carrental.models import CarBrends, CarModels, CarPrice, CarYear, Review, Cars, CarRentai, Booking, Manzil1, Manzil2

# Register your models here.
admin.site.register(CarRentai)
admin.site.register(CarBrends)
admin.site.register(CarModels)
admin.site.register(CarPrice)
admin.site.register(Manzil1)
admin.site.register(Manzil2)
admin.site.register(CarYear)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Cars)