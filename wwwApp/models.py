from django.db import models

# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=50, verbose_name="Lotnisko")

class Plane(models.Model):
    name = models.CharField(max_length=50, verbose_name="Samolot")
    passengers_limit = models.IntegerField()

class Flight(models.Model):
    starting_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="start_airporl_to_airport")
    starting_time = models.DateTimeField(verbose_name="Czas odlotu")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dest_airport_to_airport")
    destination_time= models.DateTimeField(verbose_name="Czas dotarcia")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, verbose_name="Samolot")

class Passenger(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="passenger_to_flight")
    name = models.CharField(max_length=50, verbose_name="Imie")
    surname = models.CharField(max_length=50, verbose_name="Nazwisko")



