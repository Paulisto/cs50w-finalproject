from django import forms
from django.forms import modelformset_factory

from .models import Trip, Activity, Review, Expense

# Model form for creating a new trip
class NewTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'start_date', 'end_date', 'budget']
        widgets = {
            'destination': forms.Select(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'class':'form-control inline-date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class':'form-control inline-date', 'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class':'form-control'})
        }
        
        labels = {
            'destination': 'Select destination',
            'budget': 'Enter your budget'
        }

# Model form for creating an itinerary
class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'date', 'time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'name': 'Activity Name:',
            'description': 'Details'
        }

# Helps create multiple forms
ItineraryFormSet = modelformset_factory(
    Activity,
    form=ItineraryForm,
    extra=6,  # Number of empty forms to display initially
    can_delete=True # Enables deletion of activities
)

# Model form for writing a review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
           'rating': forms.HiddenInput(attrs={'id': 'rating-input'}),
           'comment': forms.Textarea(attrs={'rows':3, 'max-length': 5000, 'class':'form-control', 'placeholder': "Write what you think of the place (optional)"}) 
        }

        labels = {
            'rating': "Rating"
        }

# Adds or edits expenses for the trip
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        
        labels = {
            'description': "Name",
            'amount': "Enter the cost (UGX)",
        } 
        
ExpenseFormSet = modelformset_factory(
    Expense,
    form=ExpenseForm,
    extra=4,  # Number of empty forms to display initially
    can_delete=True # Enables deletion of expenses 
)
