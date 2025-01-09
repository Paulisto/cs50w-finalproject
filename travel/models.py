from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


# User model
class User(AbstractUser):
    pass

class Destination(models.Model):
    REGION_CHOICES = (
        ("AFR", "Africa"),
        ("ASIME", "Asia and Middle East"),
        ("EUR", "Europe"),
        ("OCE", "Oceania"),
        ("NAC", "North and Central America & Caribbean"),
        ("SOA", "South America")
    )
           
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Optional description
    location = models.CharField(max_length=255, blank=True)  # General location (e.g., city, country)
    latitude = models.FloatField(blank=True, null=True)  # Used if the destination has a specific point on the map
    longitude = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('city', 'City'), ('landmark', 'Landmark'), ('island', 'Island'), ('province', 'Province'), ('country', 'Country')], default='city')
    destination_image = models.ImageField(upload_to='destination_images/', blank=True, null=True)
    region = models.CharField(max_length=5, choices=REGION_CHOICES, default="AFR")
    image_attribution = models.CharField(max_length=255, blank=True, null=True) # Image source (Important to give credit)
    
    def __str__(self):
        return f"{self.name}, {self.location}"
    
    # Calculates the average rating for each destination
    def average_rating(self):
        average = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average else "No ratings yet"
        
    
    class Meta:
        ordering = ['region', 'name']

# Model for attractions found in each destination        
class Attraction(models.Model):
    name = models.CharField(max_length=255)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    attraction_image = models.ImageField(upload_to='attraction_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} found in {self.destination}"
    
       
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=0)
    
    def total_expenses(self):
        return sum(expense.amount for expense in self.expense_set.all())
    
    def remaining_budget(self):
        return self.budget - self.total_expenses()
    
class Activity(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True) # Optional description
    date = models.DateField()
    time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"
    
class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateField()
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()  # e.g., 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} rated {self.destination} {self.rating} stars."
    
    class Meta:
        unique_together = ('user', 'destination')