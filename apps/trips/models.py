from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
# from django.contrib.auth.models import AbstractUser, User


class Trip(models.Model):
    destination = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1000, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    planner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='added_trips')
    travelers = models.ManyToManyField(get_user_model(), related_name='joined_trips')

    def __repr__(self):
        return "Trip: {}".format(self.destination)
