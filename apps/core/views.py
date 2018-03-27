# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import (
    logout,
    login,
)
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import ugettext_lazy as _

from forms import *

User = get_user_model()


def index(request):
    return HttpResponse("working on it...from core")


# User form AND Profile
# @login_required
@transaction.atomic
def register_profile(request):
    if request.user.is_authenticated:
        print "already logged in. Sending to dashboard"
        return HttpResponse("{}, you're already logged in.".format(request.user.first_name))

    print "Not logged in...moving to get form"

    title = "Register"
    button_text = "Register"
    user_form = UserRegisterForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    alt_link = "/login"
    alt_message = "login"

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': title,
        'button_text': button_text,
        'alt_message': alt_message,
        'alt_link': alt_link,
    }

    if user_form.is_valid() and profile_form.is_valid():
        print "user and profile forms were valid...now trying to save to db"
        user = user_form.save(commit=False)
        password = user_form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        print "Saved user to DB...now to get profile"
        user.profile.alias = profile_form.cleaned_data.get('alias')
        user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
        user.profile.save()
        login(request, user)
        print("is authenticated?: ", request.user.is_authenticated())
        messages.success(request, _('Profile successfully created!'))

        return redirect('/trips/home')

    return render(request, 'form.html', context)


def login_view(request):
    print "reached login view"
    print("Arrived at login. Is user authenticated? ",
          request.user.is_authenticated())
    if request.user.is_authenticated:
        print "Logged in as {}".format(request.user.first_name)
        print "already logged in. Sending to dashboard"
        return redirect('/trips/home')

    user_form = UserLoginForm(request.POST or None)
    title = "Login"
    button_text = "Login"
    alt_link = "/register"
    alt_message = "register"
    context = {
        'user_form': user_form,
        'title': title,
        'button_text': button_text,
        'alt_message': alt_message,
        'alt_link': alt_link,
    }

    if user_form.is_valid():
        email = user_form.cleaned_data.get('email')
        password = user_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        print "user:", user
        print "logging in..."
        login(request, user)
        print("user is authenticated: ", request.user.is_authenticated())
        # return render(request, 'dashboard.html', context)
        return redirect('/trips/home')

    return render(request, 'form.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    print "reached update_profile view"
    # if request.user.is_superuser: #THIS LINE SHOULD BE UNCOMMENTED WHEN APP IS DONE
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _(
                'Your profile was successfully updated!'))
            print("successfully submitted the update form")
            return redirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))

    current_user = request.user
    user_form = UserForm(instance=current_user)
    profile_form = ProfileForm(instance=current_user.profile)
    return redirect('/login')
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def logout_view(request):
    print "reached logout view"
    name = request.user.first_name
    logout(request)
    return redirect('/login')
    return HttpResponse("You successfully logged out, {}. See you next time!".format(name))
