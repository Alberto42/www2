from django.db import models

# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=50, verbose_name="Lotnisko")
    passengers_limit = models.IntegerField()

class Plane(models.Model):
    name = models.CharField(max_length=50, verbose_name="Samolot")

class Flight(models.Model):
    starting_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="start_airporl_to_airport")
    starting_time = models.DateTimeField(verbose_name="Czas odlotu")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dest_airport_to_airport")
    destination_time= models.DateTimeField(verbose_name="Czas dotarcia")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, verbose_name="Samolot")


