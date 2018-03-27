# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms import *


# Create your views here.
@login_required
def home_view(request):
    print "reached  home view. If they are logged in, show the dashboard"
    # print "logged in as {}".format(request.user.first_name)

    all_trips = Trip.objects.all()
    joined_trips = Trip.objects.filter(travelers=request.user)
    joined_trips = Trip.objects.filter(travelers=request.user).order_by('start_date')
    available_trips = Trip.objects.exclude(travelers=request.user)

    print ("joined trips:", joined_trips.all())
    # available_trips = Trip.objects.exclude(planner=request.user)

    context = {
        'greeting_name': request.user.profile.alias,
        # 'submission_form': trip_form,
        # 'button_text': button_text,
        # 'title': title,
        'available_trips': available_trips,
        'joined_trips': joined_trips,

    }
    return render(request, 'dashboard.html', context)


@login_required
def add_trip(request):
    print "REACHED ADD TRIP"
    print "logged in as {}".format(request.user.first_name)

    button_text = "Add this trip!"
    title = "Add a trip!"

    trip_form = TripForm(request.POST or None)

    if trip_form.is_valid():
        destination = trip_form.cleaned_data.get('destination')
        description = trip_form.cleaned_data.get('description')
        start_date = trip_form.cleaned_data.get('start_date')
        end_date = trip_form.cleaned_data.get('end_date')

        user = request.user
        new_trip = Trip.objects.create(destination=destination, description=description, planner=user,
                                       start_date=start_date, end_date=end_date)
        # if you wanted to let people plan trips without adding themselves, then comment OUT the line below
        new_trip.travelers.add(user)
        new_trip.save()

        print "added trip to db: {}".format(Trip.objects.last())
        return redirect('/trips/home')
    context = {
        'greeting_name': request.user.profile.alias,
        'submission_form': trip_form,
        'button_text': button_text,
        'title': title,
        # 'available_trips': available_trips,
        # 'joined_trips': joined_trips,

    }

    return render(request, 'submission_form.html', context)


@login_required
def get_trips_by_user(request, user_id):
    trip_set = Trip.objects.filter(planner=user_id)
    trip_count = trip_set.count()
    planner = User.objects.get(id=user_id)

    print "count: ", trip_count
    print "trip set:", trip_set

    context = {
        'planner_name': planner.profile.alias,
        'trip_set': trip_set,
        'trip_count': trip_count,
    }

    return render(request, 'all_trips_by_user.html', context)


@login_required
def delete_trip(request, trip_id):
    # Trip.objects.all().delete()
    del_trip = Trip.objects.get(id=trip_id)
    if request.user == del_trip.planner:
        Trip.objects.get(id=trip_id).delete()
        print "trip removed forever"

    return redirect('/')


@login_required
def join_trip(request, trip_id):
    print "reached JOIN TRIP"
    # this is going to TOGGLE the traveler on the trip or not
    current_trip = Trip.objects.get(id=trip_id)
    print "trip: ", current_trip.description

    current_trip_travelers = Trip.objects.get(id=trip_id).travelers.all()
    print "Travelers:", current_trip_travelers

    # if the trip is already a joined, then make it UN-joined
    for user in current_trip_travelers:
        print "user info:", user.id
        if user.id == request.user.id:
            current_trip.travelers.remove(request.user)
            current_trip.save()
            return redirect('/trips')

    # otherwise add them to the trip
    current_trip.travelers.add(request.user)
    current_trip.save()

    # new_trip = Trip.objects.get(id=trip_id)

    return redirect('/')


@login_required
def view_trip(request, trip_id):
    current_trip = Trip.objects.get(id=trip_id)
    travelers = current_trip.travelers.all()
    context = {
        'trip': current_trip,
        'travelers': travelers,

    }
    return render(request, 'show_trip.html', context)
