from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_dashboard", views.dashboard, name="dashboard"),
    path("new_trip", views.newtrip, name="newtrip"),
    path("trip/<int:trip_id>", views.trip, name="trip"),
    path("create_itinerary/<int:trip_id>", views.create_itinerary, name="createitinerary"),
    path("edit_itinerary/<int:trip_id>", views.edit_itinerary, name="edititinerary"),
    path("edit_budget/<int:trip_id>", views.edit_budget, name="editbudget"),
    path("destinations", views.destination_list, name="destinations"),
    path("destination/<int:destination_id>", views.destination, name="destination"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addreview/<int:destination_id>", views.add_review, name="addreview")
]
