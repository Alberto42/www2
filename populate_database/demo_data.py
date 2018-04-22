import logging
import os
import random
from datetime import datetime
from datetime import timedelta

from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WWW2e.settings")
setup()

from populate_database.planes import planes
from populate_database.airports import airports
from wwwApp.models import *
from itertools import cycle

SIZE = 50;
PLANES_COUNT = SIZE
AIRPORTS_COUNT = SIZE
FLIGHTS_FOR_EACH_PLANE_COUNT = 5

Plane.objects.all().delete()
Flight.objects.all().delete()
Airport.objects.all().delete()

random.seed(42)

logging.basicConfig(level=logging.INFO)

logging.info("Create planes:")
for (plane, i) in zip(cycle(planes), range(0, PLANES_COUNT)):
    Plane.objects.create(name=plane, passengers_limit=random.randrange(20, 60))

logging.info("Create airports:")
for (airport, i) in zip(cycle(airports), range(0, AIRPORTS_COUNT)):
    Airport.objects.create(name=airport)

logging.info("Create flights:")
i=0
for plane in Plane.objects.all():
    logging.info("Flights for plane: " + str(i))
    start_airport = random.choice(tuple(Airport.objects.all()))
    end_date = datetime(2018, 5, 1, 0, 0) + timedelta(minutes=random.randrange(0, 300))
    for i in range(0, FLIGHTS_FOR_EACH_PLANE_COUNT):
        destination_airport = start_airport
        while (destination_airport == start_airport):
            destination_airport = random.choice(tuple(Airport.objects.all()))

        start_date = end_date + timedelta(minutes=random.randrange(300, 720))
        end_date = start_date + timedelta(minutes=random.randrange(30, 180))

        Flight.objects.create(starting_airport=start_airport,
                              starting_time=start_date,
                              destination_airport=destination_airport,
                              destination_time=end_date,
                              plane=plane)

        start_airport = destination_airport

logging.info("Create passengers:")
i = 0
for flight in Flight.objects.all():
    logging.info("Passengers if Flight: " + str(i))
    seats_taken = max(0,flight.plane.passengers_limit-random.randrange(1,60))
    for i in range(seats_taken):
        Passenger.objects.create(flight=flight,name="Passenger_name_" + str(i),
                                 surname= "Passenger_surname_" + str(i))