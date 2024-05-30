from rest_framework import serializers
from .models import Drink
from .models import Target
from .models import Flight
from .models import User

class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['id', 'name', 'description']


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'date', 'title', 'predictor', 'company', 'targetPrice', 'accuracy']

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'fromAirport', 'toAirport', 'date', 'airline', 'departs', 'arrives', 'arriveDateChg']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userName', 'passwordHash']        