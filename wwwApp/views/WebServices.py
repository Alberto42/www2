from datetime import timedelta

from django.http import JsonResponse
from django.utils.datetime_safe import datetime
from rest_framework import serializers

from wwwApp.models import Flight, Crew
from wwwApp.utils import flight_intersect_crew_flights


def AddRelationWebService(request):
    crew_id = request.GET["crew_id"]
    flight_id = request.GET["flight_id"]
    flight = Flight.objects.get(id=flight_id)
    crew = Crew.objects.get(id=crew_id)
    crew_flights = Flight.objects.filter(crew=crew)
    if flight_intersect_crew_flights(crew_flights, flight):
        response = {'alert_class': 'alert-danger', 'alert': 'Porażka! Załoga w tym czasie pracuje w innym samolocie'}
    else:
        flight.crew = crew
        flight.save()
        response = {'alert_class': 'alert-success', 'alert': 'Sukces! Udało się pomyślnie dodać załogę do lotu'}

    return JsonResponse(response)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


def CrewRestWebService(request):
    crews = Crew.objects.all()
    serializer = CrewSerializer(crews, many=True)
    return JsonResponse(serializer.data, safe=False)


class FlightsSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Flight
        fields = (
            'id', 'starting_airport_name', 'starting_time', 'destination_airport_name', 'destination_time', 'crew_name',
            'starting_time_formatted', 'destination_time_formatted')


def FlightRestWebService(request):
    if 'date' in request.GET:
        flights = flights_filtered_by_date(request)
    else:
        flights = Flight.objects.all()
    serializer = FlightsSerializer(flights, many=True)
    return JsonResponse(serializer.data, safe=False)


def flights_filtered_by_date(request):
    format = '%Y-%m-%d'
    date_str = request.GET["date"]
    day = datetime.strptime(date_str, format)
    next_day = day + timedelta(days=1)
    flights = Flight.objects.filter(starting_time__range=[day.strftime(format), next_day.strftime(format)])
    return flights