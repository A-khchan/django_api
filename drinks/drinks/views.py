from django.http import JsonResponse
from .models import Drink
from .models import Target
from .models import Flight
from .models import User
from .serializers import DrinkSerializer
from .serializers import TargetSerializer
from .serializers import FlightSerializer
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from django.shortcuts import render

from drinks.ff import multiSearch
import json
from datetime import datetime, timedelta, date

import bcrypt

from django.http import HttpResponse
from django.template import loader

# Need this: pip install python-socketio, not pip install socketio
# import socketio

# # standard Python
# sio = socketio.Client()

# @sio.on('my message')
# def on_message(data):
#     print('I received a message!')

# @sio.on('Number of rider')
# def on_message(data):
#     print('Number of rider is: ', data)

# @sio.on('*')
# def catch_all(event, data):
#     pass

# @sio.event
# def connect():
#     print("I'm connected!")

# @sio.event
# def connect_error(data):
#     print("The connection failed!")

# @sio.event
# def disconnect():
#     print("I'm disconnected!")

# sio.connect('http://localhost:3001')

# print('my sid is', sio.sid)


@api_view(['GET', 'POST'])
def drink_list(request, format=None):
    #get all the drinks
    #serialize them
    #return json

    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        #return JsonResponse({"drinks":serializer.data}, safe=False)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id, format=None):

    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def target_list(request, format=None):
    #get all the targets
    #serialize them
    #return json

    if request.method == 'GET':
        targets = Target.objects.all()
        serializer = TargetSerializer(targets, many=True)
        #return JsonResponse({"targets":serializer.data}, safe=False)
        return Response(serializer.data)
    
    if request.method == 'POST':
        print("requesst.data is ")
        print(request.data)
        serializer = TargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("serializer return invalid")

@api_view(['GET', 'PUT', 'DELETE'])
def target_detail(request, id, format=None):

    try:
        target = Target.objects.get(pk=id)
    except Target.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TargetSerializer(target)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TargetSerializer(target, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TargetListView(generics.ListAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']



@api_view(['GET', 'POST'])
def flight_list(request, format=None):
    #get all the flights
    #serialize them
    #return json

    if request.method == 'GET':
        flights = Flight.objects.all()
        #print("flights: ", flights)
        serializer = FlightSerializer(flights, many=True)
        #return JsonResponse({"flights":serializer.data}, safe=False)
        #print("serializer.data: ", serializer.data)
        return Response(serializer.data)
    
    if request.method == 'POST':
        print("requesst.data is ")
        print(request.data)
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("serializer return invalid")

@api_view(['GET', 'PUT', 'DELETE'])
def flight_detail(request, id, format=None):

    try:
        flight = Flight.objects.get(pk=id)
    except Flight.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FlightSerializer(flight)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightListView(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['fromAirport']

@api_view(['GET', 'POST'])
def invokeFF(request, format=None):
    print("request.data is: ", request.data)
    #return Response(status=status.HTTP_204_NO_CONTENT)

    # data = [
    #     {"message": "Thank you for your submission", "date": "2023-09-01"},
    #     {"key": "hello"}
    # ]

    print("type of request.data is: ", type(request.data))

    dict = request.data
    print("dict['fromAirportList'] is: ", dict["fromAirportList"])

    print("type of dict['departFrom'] is ", type(dict["departFrom"]))

    #departFromStr = dict["departFrom"]

    departFrom = date(int(dict["departFrom"][0:4]), int(dict["departFrom"][5:7]), int(dict["departFrom"][8:]))
    departTo = date(int(dict["departTo"][0:4]), int(dict["departTo"][5:7]), int(dict["departTo"][8:]))

    data = multiSearch(dict["fromAirportList"], dict["toAirportList"],
                       departFrom, departTo)

    print("result data is: ", data)

    return JsonResponse(data, safe=False)

def registerForm(request):
    # user = User.objects.all()
    # print("user is: ", user)
    # print("user[0].userName is: ", user[0].userName)
    # print("user[0].userName is: ", user[0].passwordHash)
    # print("user[1].userName is: ", user[1].userName)
    # print("user[1].userName is: ", user[1].passwordHash)

    return render(request, 'registerForm.html')

def register(request):

    if request.method == 'POST':
        print("request method is POST")
        print("request.POST is: ", request.POST)
        print("request.POST['username'] is: ", request.POST['username'])
        print("request.POST['password'] is: ", request.POST['password'])
        userExists = User.objects.filter(userName=request.POST['username']).exists()
        if not userExists:
            print("user does not exist")
            password = bytes(request.POST['password'], 'utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)

            # Cannot use UserSerializer() and save() function to add to db
            # Serializer will make the binary data to blank.
            userObj = User.objects.create(userName = request.POST['username'], 
                                          passwordHash = hashed)
            userObj.save()

    return render(request, 'thank_register.html')


def login(request):
    # userName = request.COOKIES.get('userName')
    userName = request.session.get('userName')
    print("userName retrieved is: ", userName)
    if userName:
        print("userName found")
        context = {
            'userName': userName
        }
        template = loader.get_template('landing.html')
        response = HttpResponse(template.render(context, request))
    else:
        print("userName not found")
        response = render(request, 'login.html')

    return response

def doLogin(request):

    if request.method == 'POST':
        userExists = User.objects.filter(userName=request.POST['username']).exists()
        if userExists:
            user = User.objects.filter(userName=request.POST['username']).first()
            password = bytes(request.POST['password'], 'utf-8')

            result = bcrypt.checkpw(password, user.passwordHash)

            template = loader.get_template('landing.html')
            if result:
                print("Password correct")
                context = {
                    'userName': user.userName
                }
                request.session['userName'] = user.userName
                response = HttpResponse(template.render(context, request))
                # response.set_cookie(key='userName', value=user.userName)

            else:
                print("Password incorrect")
                context = {
                    'userName': 'N/A'
                }
                response = HttpResponse(template.render(context, request))
                

    return response


def logout(request):

    response = render(request, 'login.html')
    # response.delete_cookie('userName')
    try:
        del request.session['userName']
    except KeyError:
        pass

    return response    

def ride(request):

    userName = request.session.get('userName')
    # if userName:
    #     sio.emit('join', 'rider')

    print("userName retrieved is: ", userName)
    context = {
        'userName': userName
    }
    template = loader.get_template('ride.html')
    response = HttpResponse(template.render(context, request))

    return response