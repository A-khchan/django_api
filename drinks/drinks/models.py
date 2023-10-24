from django.db import models


class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' ' + self.description
    
class Target(models.Model):
    date = models.CharField(max_length=10)
    title = models.CharField(max_length=1000)
    predictor = models.CharField(max_length=100)
    company = models.CharField(max_length=300)
    targetPrice = models.FloatField()
    accuracy = models.FloatField()
    
class Flight(models.Model):
    fromAirport = models.CharField(max_length=3)
    toAirport = models.CharField(max_length=3)
    date = models.CharField(max_length=10)
    airline = models.CharField(max_length=100)
    departs = models.CharField(max_length=8)
    arrives = models.CharField(max_length=8)
    arriveDateChg = models.IntegerField()

