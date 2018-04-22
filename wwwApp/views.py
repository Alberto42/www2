import datetime
import locale

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
class PassangersTable(tables.Table):
    class Meta:
        model = Passenger
        template_name = 'django_tables2/bootstrap.html'
        exclude=['id', 'flight']

def buy_ticket(request):
    flight = Flight.objects.get(id=request.POST['id'])
    Passenger.objects.create(flight=flight, name=request.POST['name'], surname=request.POST['surname'])
    return redirect(flight_details,request.POST['id'])

def flight_details(request, id):
    flight = Flight.objects.get(id=id)

    flight.starting_time = FlightTable.render_starting_time(None, flight)
    flight.destination_time = FlightTable.render_destination_time(None, flight)

    passengers = Passenger.objects.filter(flight=flight)
    table = PassangersTable(passengers)
    RequestConfig(request).configure(table)
    return auth_views.login(request, template_name='wwwApp/details.html', redirect_field_name='home',
                            extra_context={'user': str(request.user), 'flight': flight, 'table': table,
                                           'taken_seats' : len(passengers),
                                           'free_seats' : flight.plane.passengers_limit - len(passengers)})

def home(request):
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    table = FlightTable(Flight.objects.all())
    RequestConfig(request).configure(table)
    return auth_views.login(request,template_name='wwwApp/home.html',redirect_field_name='home',
                            extra_context={'user' : str(request.user),'table': table})

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