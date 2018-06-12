from datetime import timedelta

from django.db import transaction
from django.db.transaction import rollback
from django.http import JsonResponse, HttpResponse
from django.utils.datetime_safe import datetime
from rest_framework import serializers

from wwwApp.models import Flight, Crew
from wwwApp.utils import flight_intersect_crew_flights, intersect


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

def RemoveCrewWebService(request):
    flight_id = request.GET["flight_id"]
    flight = Flight.objects.get(id=flight_id)
    flight.crew = None
    flight.save()
    return JsonResponse({})

class Request:
    pass

@transaction.atomic
def SynchronizeWebService(request):
    sid = transaction.savepoint()
    requests = []
    for i,(key,value) in enumerate(request.GET.items()):
        if (i % 2 == 1):
            requests[-1].flight_id = int(value)
        else:
            requests.append(Request())
            if (value == 'remove'):
                requests[-1].remove = True
            else:
                requests[-1].remove = False

                requests[-1].crew_id = int(value)

    sid = transaction.savepoint()
    wrong_flights = set()
    for r in requests:
        flight = Flight.objects.get(id=r.flight_id)
        if (r.remove):
            flight.crew = None
            flight.save()
        else:
            crew = Crew.objects.get(id=r.crew_id)
            flight.crew = crew
            flight.save()

    for r in requests:
        if (r.remove == False):
            crew = Crew.objects.get(id=r.crew_id)
            crew_flights = Flight.objects.filter(crew=crew)
            for flight1 in crew_flights:
                for flight2 in crew_flights:
                    if (flight1 != flight2 and intersect(flight1,flight2)):
                        wrong_flights.add(flight1)
                        wrong_flights.add(flight2)
    if (wrong_flights):
        transaction.savepoint_rollback(sid)

    serializer = FlightsSerializer(wrong_flights, many=True)
    return JsonResponse(serializer.data, safe=False)

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