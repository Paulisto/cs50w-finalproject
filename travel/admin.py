from django.contrib import admin
from .models import User, Destination, Attraction, Trip, Activity, Expense, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Destination)
admin.site.register(Attraction)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Expense)
admin.site.register(Review)