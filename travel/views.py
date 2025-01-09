from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages # imports messages

from .models import User, Destination, Attraction, Review, Trip, Activity, Expense
from .forms import NewTripForm, ItineraryForm, ItineraryFormSet, ReviewForm, ExpenseForm

# For guest users and non-authenticated users
def index(request):
    # If the user is already authenticated, redirect them to the dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    
    # For displaying the popular destinations - limits up to 5
    destinations = Destination.objects.all()[:5]
    
    # Otherwise, render the guest landing page
    return render(request, "travel/index.html", {
        "destinations": destinations
    })

# For authenticated users
@login_required    
def dashboard(request):
     # If the user is authenticated, render the dashboard
    if request.user.is_authenticated:
        # You can fetch user-specific data here, like trips, itinerary, etc.
        trips = request.user.trip_set.all()  # Assuming a ForeignKey from Trip to User
        context = {
            'trips': trips,
        }
        return render(request, "travel/dashboard.html", context)
    else:
        # If not authenticated, redirect to the guest home page
        return HttpResponseRedirect(reverse("index"))

# Displays all the available destinations
def destination_list(request):
    destinations = Destination.objects.all()  # Fetch all destinations from the database
    return render(request, 'travel/destination_list.html', {'destinations': destinations})

# Displays destination guides for each destination
def destination(request, destination_id):
    
    # Looks up the destination guide
    destination = Destination.objects.get(pk = destination_id)
    
    # Looks up the attractions attached to each destination
    attractions = Attraction.objects.filter(destination=destination_id)
    
    # Looks up all the reviews for each destination
    reviews = Review.objects.filter(destination=destination_id)
   
    user_review = None
    
    average_rating = destination.average_rating()
    total_reviews = reviews.count() + (1 if user_review else 0)
    
    if request.user.is_authenticated:
        # Fetches the logged-in user's review if it exists
        user_review = Review.objects.filter(user=request.user, destination=destination).first()
    
    reviews = Review.objects.filter(destination=destination).exclude(user=request.user if request.user.is_authenticated else None)
    
    # Handle review form submission
    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.destination = destination
            form.save()
            return redirect('destination', destination_id=destination.id)
    else:
        form = ReviewForm(instance=user_review)
        
    return render(request, "travel/destination_guide.html", {
        "destination" : destination,
        "attractions": attractions,
        "form": ReviewForm(),
        "destination_id": destination_id,
        "reviews": reviews,
        "average_rating": average_rating,
        'user_review': user_review,
        "total_reviews": total_reviews
    })

# View for creating a new trip
@login_required
def newtrip(request):
    destination_id = request.GET.get('destination_id')  # Get destination ID from query parameters

    if request.method == "POST":
        form = NewTripForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            new_trip = form.save()
            return HttpResponseRedirect(reverse("trip", args=(new_trip.pk,)))
    else:
        if destination_id:
            try:
                # Pre-selects destination if destination_id is passed
                destination = Destination.objects.get(pk=destination_id)
                form = NewTripForm(initial={'destination': destination})
            except Destination.DoesNotExist:
                form = NewTripForm()  # fallback if destination is invalid
        else:
            form = NewTripForm()

    return render(request, 'travel/newtrip.html', {
        'form': form
    })

# View for trip details
@login_required
def trip(request, trip_id):
    
    # Retrieves relevant information from the database
    trip = Trip.objects.get(pk=trip_id)
    activities = Activity.objects.filter(trip=trip).order_by("date", "time")
    expenses = Expense.objects.filter(trip=trip)
    total_expenses = trip.total_expenses()
    remaining_budget = trip.remaining_budget()
    
    return render(request, 'travel/trip.html', {
        'trip': trip,
        'activities': activities,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget
    })

# View for creating an itinerary
@login_required
def create_itinerary(request, trip_id):
    
    trip = Trip.objects.get(pk=trip_id)
    
    if request.method == "POST":
        formset = ItineraryFormSet(request.POST, queryset=Activity.objects.filter(trip=trip))
        
        if formset.is_valid():
            activities = formset.save(commit=False)
            for activity in activities:
                activity.trip = trip  # assigns the trip to each activity
                activity.save()
                print(f"Saved activity: {activity.name} for trip {trip.id}")
            return HttpResponseRedirect(reverse('trip', args=(trip_id,)))
        else:
            print(formset.errors) # Prints errors for debugging     
    else:
        formset = ItineraryFormSet(queryset=Activity.objects.none())
        
    return render(request, 'travel/create_itinerary.html', {'trip': trip, 'formset': formset})
        
@login_required
def edit_itinerary(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
     
    # Set up a formset for editing multiple activities at once
    ItineraryFormSet = modelformset_factory(Activity, form=ItineraryForm, extra=2, can_delete=True)
    activities = Activity.objects.filter(trip=trip).order_by("date", "time")
    
    if request.method == "POST":
        formset = ItineraryFormSet(request.POST, queryset=activities)
        if formset.is_valid():
            formset.save()  # Saves each form in the formset
            return redirect("trip", trip_id=trip.id)
    else:
        formset = ItineraryFormSet(queryset=activities)
        
    return render(request, "travel/edit_itinerary.html", {
        "trip": trip,
        "formset": formset,
    })
    
#view for adding and editing expenses
@login_required
def edit_budget(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    expenses = Expense.objects.filter(trip=trip)
    
    ExpenseFormSet = modelformset_factory(Expense, form=ExpenseForm, extra=2, can_delete=True)
    
    if request.method == "POST":
        formset = ExpenseFormSet(request.POST, queryset=expenses)
        if formset.is_valid():
            # Save each form with the associated trip
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                    expense = form.save(commit=False)
                    expense.trip = trip  # Ensure trip is set
                    expense.save()
                elif form.cleaned_data.get("DELETE") and form.instance.pk:
                    form.instance.delete()  # Delete the expense if marked
            return redirect("trip", trip_id=trip.id)
    else:
        formset = ExpenseFormSet(queryset=expenses)
    
    return render(request, "travel/edit_budget.html", {
        "trip": trip,
        "formset": formset
    })
            
# View for users adding a review for each destination
@login_required
def add_review(request, destination_id):
    if request.method == "POST":
    
        destination = Destination.objects.get(pk=destination_id)
            
        form = ReviewForm(request.POST)
        
        if form.is_valid():

            form.instance.user = request.user
            form.instance.destination = destination

    
            form.save()
            
            return HttpResponseRedirect(reverse("destination", args=(destination_id,)))
      
# View for logging in  
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)


        # Check if user is authenticated
        if user is not None:
            login(request, user)
            # Redirect to dashboard if authenticated
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid username and/or password')
            return render(request, "travel/login.html")
    else:
        # If user is already logged in, redirect to dashboard
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        
        # Otherwise, display the login page
        return render(request, "travel/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return render(request, "network/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel/register.html")     