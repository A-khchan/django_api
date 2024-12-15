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

class User(models.Model):
    userName = models.CharField(max_length=100)
    passwordHash = models.BinaryField()
    recoveryCode = models.BinaryField(blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)

class Post(models.Model):
    date = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    replyID = models.TextField(blank=True, null=True)

class Delivery(models.Model):
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=10)
    deliveryDate = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    selfPickup = models.CharField(max_length=1)
    parentID = models.IntegerField()
    repeatFreq = models.CharField(max_length=50)
    eligible = models.CharField(max_length=1)
    ticketNo = models.IntegerField()
    leaveAtDoor = models.CharField(max_length=1)
    phoneForPic = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10)
    log = models.CharField(max_length=200, blank=True, null=True)
    comments = models.CharField(max_length=300, blank=True, null=True)
    seq = models.FloatField()

class DeliveryItems(models.Model):
    deliveryID = models.IntegerField()
    item = models.CharField(max_length=20)
    quantity1 = models.IntegerField()
    quantity2 = models.IntegerField()

class DeliveredItems(models.Model):
    deliveryID = models.IntegerField()
    item = models.CharField(max_length=20)
    quantity1 = models.IntegerField()
    quantity2 = models.IntegerField()