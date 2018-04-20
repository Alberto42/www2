import datetime
import locale

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_tables2 import tables, RequestConfig
import django_tables2 as tables

from wwwApp.models import *
# Create your views here.

class FlightTable(tables.Table):
    starting_airport = tables.Column(verbose_name="Lotnisko startowe", accessor="starting_airport.name")
    destination_airport = tables.Column(verbose_name="Lotnisko docelowe", accessor="destination_airport.name")
    plane = tables.Column(accessor="plane.name")
    def render_starting_time(self, record):
        locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
        return record.starting_time.strftime("%a, %d %b %Y %H:%M:%S")
    def render_destination_time(self, record):
        locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
        return record.destination_time.strftime("%a, %d %b %Y %H:%M:%S")
    class Meta:
        model = Flight
        template_name = 'django_tables2/bootstrap.html'
        exclude=['id']
        row_attrs = {
            'flight-id': lambda record: str(record.id)
        }

def flight_table(request):
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    table = FlightTable(Flight.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'wwwApp/flights.html', {'table': table})


def flight_details(request, id):
    return HttpResponse('')

def home(request):
    return HttpResponse('')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = UserCreationForm()
    return render(request, 'wwwApp/signup.html', {'form': form})