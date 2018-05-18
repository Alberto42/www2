import datetime
import locale
from django.contrib.auth import login, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django_tables2 import tables, RequestConfig
import django_tables2 as tables

from django import forms
from django.contrib.auth import (
    authenticate,
)

from django.utils.translation import gettext, gettext_lazy as _
from rest_framework import serializers

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
        exclude = ['id']
        row_attrs = {
            'flight-id': lambda record: str(record.id)
        }


class PassangersTable(tables.Table):
    class Meta:
        model = Passenger
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id', 'flight']


def home(request):
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    table = FlightTable(Flight.objects.all())
    RequestConfig(request).configure(table)
    return auth_views.login(request, template_name='wwwApp/home.html', redirect_field_name='home',
                            extra_context={'user': str(request.user), 'table': table})


def flight_details(request, id):
    flight = Flight.objects.get(id=id)

    flight.starting_time = FlightTable.render_starting_time(None, flight)
    flight.destination_time = FlightTable.render_destination_time(None, flight)

    passengers = Passenger.objects.filter(flight=flight)
    table = PassangersTable(passengers)
    RequestConfig(request).configure(table)
    return auth_views.login(request, template_name='wwwApp/details.html', redirect_field_name='home',
                            extra_context={'user': str(request.user), 'flight': flight, 'table': table,
                                           'taken_seats': len(passengers),
                                           'free_seats': flight.plane.passengers_limit - len(passengers)})


class UserCreationFormPl(UserCreationForm):
    password1 = forms.CharField(
        label=_("Hasło"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Potwierdzenie hasła"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

def signup(request):
    if request.method == 'POST':
        form = UserCreationFormPl(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = UserCreationFormPl()
    return render(request, 'wwwApp/signup.html', {'form': form})


def buy_ticket(request):
    flight = Flight.objects.get(id=request.POST['id'])
    Passenger.objects.create(flight=flight, name=request.POST['name'], surname=request.POST['surname'])
    return redirect(flight_details, request.POST['id'])

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


def CrewRestWebService(request):
    crews = Crew.objects.all();
    serializer = CrewSerializer(crews,many=True);
    return JsonResponse(serializer.data, safe=False);

class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


def FlightRestWebService(request):
    flights = Flight.objects.all();
    serializer = FlightsSerializer(flights,many=True);
    return JsonResponse(serializer.data, safe=False);

def air_crew(request):
    return render(request, 'wwwApp/air_crew.html');