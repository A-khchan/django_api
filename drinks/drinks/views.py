from django.http import JsonResponse
from .models import Drink
from .models import Target
from .models import Flight
from .models import Post
from .models import User
from .models import Delivery
from .models import DeliveryItems
from .serializers import DrinkSerializer
from .serializers import TargetSerializer
from .serializers import FlightSerializer
from .serializers import PostSerializer
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from django.shortcuts import render

from drinks.ff import multiSearch
import json
from datetime import timedelta, date
import pytz

import bcrypt

from django.http import HttpResponse
from django.template import loader

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
from django.conf import settings

import re

import random
import string

from datetime import datetime as dt

from google.cloud import storage  # need: pip install google-cloud-storage 

from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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

postPerPage = 10

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
def post_list(request, format=None):
    #get all the posts
    #serialize them
    #return json

    if request.method == 'GET':
        posts = Post.objects.all()
        #print("posts: ", posts)
        serializer = PostSerializer(posts, many=True)
        #return JsonResponse({"posts":serializer.data}, safe=False)
        #print("serializer.data: ", serializer.data)
        return Response(serializer.data)
    
    if request.method == 'POST':
        print("requesst.data is ")
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("serializer return invalid")
            print(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id, format=None):

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        #delete the associate image from GCS bucket first
        if post.image and not post.image == "":
                # Initialize a client
                client = storage.Client()
                # Get the bucket
                bucket = client.get_bucket('offerimage-may2018.appspot.com')
                # Get the blob (file) to delete
                folder_name = 'images'
                blob = bucket.blob(f'{folder_name}/{post.image}')
                # Delete the blob
                blob.delete()

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
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


def checkLoginStatus(request, page, context=None):
# This function checks if user already logged in, 
# if so, return the 'page' as response, else return None

    userName = request.session.get('userName')
    if userName:
        if context is None:
            user = User.objects.filter(userName=request.session.get('userName')).first()
            context = {
                'placeholder': 'test',
                'nickname': user.nickname,
            }
        template = loader.get_template(page)
        response = HttpResponse(template.render(context, request))
    else:
        response = None

    return response

def registerForm(request):
    # user = User.objects.all()
    # print("user is: ", user)
    # print("user[0].userName is: ", user[0].userName)
    # print("user[0].userName is: ", user[0].passwordHash)
    # print("user[1].userName is: ", user[1].userName)
    # print("user[1].userName is: ", user[1].passwordHash)

    response = checkLoginStatus(request, 'landing.html')

    if response is None:
        print("userName not found")
        context = {
            'page': 'registerForm',
            'buttonName': 'Register'
        }
        template = loader.get_template('registerForm.html')        
        response = HttpResponse(template.render(context, request))        

    return response

def register(request):
    
    response = checkLoginStatus(request, 'landing.html')

    if response is None:    
        if request.method == 'POST':
            print("request method is POST")
            print("request.POST is: ", request.POST)
            print("request.POST['username'] is: ", request.POST['username'])
            print("request.POST['password'] is: ", request.POST['password'])

            userName=request.POST['username']
            # check userName format, it must be an email

            recoveryCode = request.POST['recoveryCode']

            userExists = User.objects.filter(userName=userName).exists()
            if is_valid_email(userName) and (not userExists or userExists and recoveryCode != ''):
                if len(request.POST['password']) < 8:
                    if userExists:
                        user = User.objects.filter(userName=request.session.get('userName')).first()
                        context = {
                            'page': 'registerForm',
                            'errMsg': 'Password must contain at least 8 characters',
                            'emailInputted': userName,
                            'buttonName': 'Reset',
                            'new': 'New ',
                            'recoveryCode': recoveryCode,
                            'nickname': user.nickname,
                        }
                    else:
                        context = {
                            'page': 'registerForm',
                            'errMsg': 'Password must contain at least 8 characters',
                            'emailInputted': userName,
                            'buttonName': 'Register'
                        }
                    template = loader.get_template('registerForm.html')
                    response = HttpResponse(template.render(context, request))            
                else:
                    password = bytes(request.POST['password'], 'utf-8')
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password, salt)

                    if userExists:
                        user = User.objects.filter(userName=request.POST['username']).first()
                        recoveryCode = bytes(request.POST['recoveryCode'], 'utf-8')

                        if user.recoveryCode == None:
                            result = False                        
                        else:
                            result = bcrypt.checkpw(recoveryCode, user.recoveryCode)

                        if result:
                            user.passwordHash = hashed
                            user.recoveryCode = None
                            user.save()

                            context = {
                                'page': 'registerForm',
                                'registerMsg': 'Your password is updated',
                                'nickname': user.nickname,
                            }
                            template = loader.get_template('thank_register.html')
                            response = HttpResponse(template.render(context, request)) 
                        else:
                            context = {
                                'page': 'registerForm',
                                'buttonName': 'Reset',
                                'new': 'New ',
                                'errMsg': 'Reset failed, link used is invalid',
                            }
                            template = loader.get_template('registerForm.html')
                            response = HttpResponse(template.render(context, request)) 
                    else:

                        # Cannot use UserSerializer() and save() function to add to db
                        # Serializer will make the binary data to blank.

                        if recoveryCode == '':
                            userObj = User.objects.create(userName = request.POST['username'], 
                                                        passwordHash = hashed,
                                                        recoveryCode = None)
                            userObj.save()
                            context = {
                                'page': 'registerForm',
                                'registerMsg': 'Thank you for registration',
                                'nickname': userObj.nickname,
                            }
                            template = loader.get_template('thank_register.html')
                        else:
                            context = {
                                'page': 'registerForm',
                                'errMsg': 'Invalid email or reset link, cannot reset',
                                'emailInputted': userName,
                                'buttonName': 'Reset',
                                'new': 'New '
                            }
                            template = loader.get_template('registerForm.html')

                        response = HttpResponse(template.render(context, request))            
            else:
                if recoveryCode != '':
                    errMsg = 'Invalid email or reset link, cannot reset'
                    buttonName = 'Reset'
                else:
                    errMsg = 'Invalid email or it has been registered'
                    buttonName = 'Register'

                context = {
                    'page': 'registerForm',
                    'errMsg': errMsg,
                    'emailInputted': userName,
                    'buttonName': buttonName
                }
                template = loader.get_template('registerForm.html')
                response = HttpResponse(template.render(context, request))            
        else:
            context = {
                'page': 'registerForm',
                'buttonName': 'Register'
            }
            template = loader.get_template('registerForm.html')
            response = HttpResponse(template.render(context, request)) 

    return response


def login(request):
    # userName = request.COOKIES.get('userName')

    response = checkLoginStatus(request, 'landing.html')

    if response is None:
        context = {
            'page': 'login'
        }
        print("userName not found")
        template = loader.get_template('login.html')
        response = HttpResponse(template.render(context, request))

    return response

def userinfo(request):

    response = checkLoginStatus(request, 'userinfo.html')

    if response is None:
        context = {
            'page': 'login',
            'errMsg': 'Please login',
        }
        template = loader.get_template('login.html')
        response = HttpResponse(template.render(context, request))

    return response

def userinfoUpdate(request):
    
    response = checkLoginStatus(request, 'login.html')

    if response is None or not request.method == 'POST':
        context = {
            'page': 'login',
            'errMsg': 'Please login',
        }
        template = loader.get_template('login.html')
        response = HttpResponse(template.render(context, request))
    else:
        nickname = request.POST['nickname']   
        user = User.objects.filter(userName=request.session['userName']).first()
        user.nickname = nickname
        user.save()
        context = {
            'errMsg': 'Info updated',
            'nickname': nickname,
        }
        template = loader.get_template('userinfo.html')
        response = HttpResponse(template.render(context, request))    

    return response

def doLogin(request):
    
    response = checkLoginStatus(request, 'landing.html')

    if response is None:
        if request.method == 'POST':
            userName=request.POST['username']
            userExists = User.objects.filter(userName=request.POST['username']).exists()
            if userExists:
                user = User.objects.filter(userName=request.POST['username']).first()
                password = bytes(request.POST['password'], 'utf-8')

                result = bcrypt.checkpw(password, user.passwordHash)

                if result:
                    template = loader.get_template('landing.html')
                    print("Password correct")
                    context = {
                        'placeholder': 'test',
                        'nickname': user.nickname,
                    }
                    request.session['userName'] = user.userName
                    response = HttpResponse(template.render(context, request))
                    # response.set_cookie(key='userName', value=user.userName)

                else:
                    template = loader.get_template('login.html')
                    print("Password incorrect")
                    context = {
                        'errMsg': 'Login error',
                        'emailInputted': userName,
                    }
                    try:
                        del request.session['userName']
                    except KeyError:
                        pass
                    response = HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('login.html')
                # request.session['errMsg'] = 'Login error'
                context = {
                    'errMsg': 'Login error',
                    'emailInputted': userName,
                }
                try:
                    del request.session['userName']
                except KeyError:
                    pass
                response = HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('login.html')
            context = {
                'placeholder': 'test'
            }
            response = HttpResponse(template.render(context, request))

    return response


def logout(request):

    try:
        del request.session['userName']
    except KeyError:
        pass

    response = render(request, 'login.html')
    # response.delete_cookie('userName')

    return response    

def ride(request):

    userName = request.session.get('userName')
    # if userName:
    #     sio.emit('join', 'rider')

    print("userName retrieved is: ", userName)
    context = {
        'placeholder': 'test'
    }
    template = loader.get_template('ride.html')
    response = HttpResponse(template.render(context, request))

    return response

def recover(request):
    
    response = checkLoginStatus(request, 'landing.html')

    if response is None:
        if request.method == 'POST':    
            userName = request.POST['username']
            if is_valid_email(userName):
                
                # check if user exist
                userExists = User.objects.filter(userName=request.POST['username']).exists()
                if userExists:

                    # Generate a random alphanumeric string of length 100
                    length = 100
                    characters = string.ascii_letters + string.digits  # Contains both letters and digits
                    random_string = ''.join(random.choice(characters) for _ in range(length))

                    recoveryCode = bytes(random_string, 'utf-8')
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(recoveryCode, salt)    

                    user = User.objects.filter(userName=request.POST['username']).first()
                    user.recoveryCode = hashed
                    user.save()

                    recoveryURL = "https://www.roboosoft.com/account/reset/?code=" + random_string 

                    html_content = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fixing the "Non-CSS MIME Types Are Not Allowed in Strict Mode" Error</title>
                <style>
                    body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    line-height: 1.6;
                    }
                    h1, h2, h3 {
                    color: #333;
                    }
                    code {
                    background-color: #f9f9f9;
                    padding: 2px 6px;
                    border-radius: 4px;
                    }
                    pre {
                    background-color: #f9f9f9;
                    padding: 10px;
                    border-left: 4px solid #ccc;
                    overflow-x: auto;
                    }
                </style>
                </head>
                <body>

                <h3>Below is your recovery link:</h3>
                <a href=" """ 

                    html_content = html_content + recoveryURL + """">"""
                    
                    html_content = html_content + recoveryURL + """</a>
                  

                </body>
                </html>
                """

                    result = sendEmail(userName, "RobooSoft - link for password reset", html_content)

                    template = loader.get_template('login.html')
                    # request.session['errMsg'] = 'Login error'
                    context = {
                        'errMsg': result,
                        'nickname': user.nickname,
                    }
                    response = HttpResponse(template.render(context, request))
                else:
                    #User does not exist
                    template = loader.get_template('registerForm.html')
                    context = {
                        'errMsg': 'User not found, please register',
                        'buttonName': 'Register',
                        'emailInputted': userName
                    }
                    response = HttpResponse(template.render(context, request))            
            else:
                #Invalid user name (email)
                template = loader.get_template('login.html')
                context = {
                    'errMsg': 'Please enter a valid email'
                }
                response = HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('login.html')
            context = {
                'placeholder': 'test'
            }
            response = HttpResponse(template.render(context, request))

    return response


def sendEmail(receiver_email, subject, html_content):
    
    result = "to be confirmed"

    sender_email = "info@roboosoft.com"
    smtp_server = "smtp.ionos.com"  # Replace with your SMTP server
    smtp_port = 587  # SMTP port for TLS (for Gmail or similar servers)
    smtp_username = "info@roboosoft.com"

    file_path = os.path.join(settings.BASE_DIR, 'drinks', 'info_smtp.txt')

    with open(file_path, 'r') as file:
        smtp_password = file.read().strip()  # Use a secure method to handle passwords

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Send the email using SMTP
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
        result = "Email sent successfully"
    except Exception as e:
        print(f"Error sending email: {e}")
        result = f"Error sending email: {e}" + ">>>" + smtp_password + "<<<"

    return result


def is_valid_email(email):
    # Regular expression for validating an email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use the re.match() method to check if the input matches the pattern
    return re.match(email_regex, email) is not None


def reset(request):
    
    response = checkLoginStatus(request, 'landing.html')

    if response is None:
        if request.method == "GET":
            recoveryCode = request.GET.get('code', 'default')
            if recoveryCode != 'default':
                context = {
                        'page': 'registerForm',
                        'buttonName': 'Reset',
                        'new': 'New ',
                        'recoveryCode': recoveryCode,
                        'registerMsg': 'RecoveryCode >>' + recoveryCode + '<<'
                    }
                template = loader.get_template('registerForm.html')
                response = HttpResponse(template.render(context, request))  
            else:
                context = {
                        'page': 'registerForm',
                        'buttonName': 'Register',
                        'registerMsg': 'RecoveryCode = default'
                    }
                template = loader.get_template('registerForm.html')
                response = HttpResponse(template.render(context, request))  
        else:
            context = {
                    'page': 'registerForm',
                    'buttonName': 'Register',
                    'registerMsg': 'method is not GET'
                }
            template = loader.get_template('registerForm.html')
            response = HttpResponse(template.render(context, request))  
                

    return response


def postform(request):

    pageNumStr = request.GET.get('page', '1')
    if pageNumStr.isdigit():
        pageNum = int(pageNumStr)
    else:
        pageNum = 1

    template = loader.get_template('postform.html')
    
    allowDel = "N"
    if request.session.get('userName') == "albert88hk@yahoo.com.hk":
        allowDel = "Y"

    if request.session.get('userName'):
        user = User.objects.filter(userName=request.session.get('userName')).first()
        nickname = user.nickname
    else:
        nickname = None

    userAll = User.objects.all()
    userDict = {}
    for i in range(0, len(userAll), 1):
        userDict[userAll[i].userName] = userAll[i].nickname

    userDict_json = json.dumps(userDict)

    context = {
        'placeholder': 'test',
        'nickname': nickname,
        'postPerPage': postPerPage,
        'pageNum': pageNum,
        'userDict': userDict_json,
        'allowDel': allowDel,
    }
    response = HttpResponse(template.render(context, request))

    return response

def post(request):
    
    response = checkLoginStatus(request, 'postform.html')

    if response is None:
        template = loader.get_template('login.html')
        context = {
            'errMsg': 'Please login to create a post'
        }
        response = HttpResponse(template.render(context, request))
    else:
        if request.method == 'POST':    
            # errMsg = ""
            # for key, value in request.POST.items():
            #     errMsg = errMsg + "Key: " + key + ", value: " + value + '\n'

            if 'image' in request.FILES:
                image = request.FILES['image']

                resized_image = resize_image(image)

                # Create a storage client
                storage_client = storage.Client()

                # Specify the bucket name
                bucket_name = 'offerimage-may2018.appspot.com'
                bucket = storage_client.bucket(bucket_name)

                # Generate a random alphanumeric string of length 100
                length = 20
                characters = string.ascii_letters + string.digits  # Contains both letters and digits
                random_string = ''.join(random.choice(characters) for _ in range(length))

                # Create a blob object with the desired file name
                blob_name = dt.now().isoformat() + random_string
                folder_name = 'images'
                blob = bucket.blob(f'{folder_name}/{blob_name}')

                # Upload the file to GCS
                blob.upload_from_file(resized_image, content_type = resized_image.content_type)
            else:
                blob_name = None

            postObj = Post.objects.create(
                            date = dt.now(pytz.utc).isoformat(),
                            author = request.session.get('userName'), 
                            title = request.POST['title'],
                            content = request.POST['content'],
                            image = blob_name,
                            replyID = None)
            postObj.save()

            allowDel = "N"
            if request.session.get('userName') == "albert88hk@yahoo.com.hk":
                allowDel = "Y"

            user = User.objects.filter(userName=request.session.get('userName')).first()

            userAll = User.objects.all()
            userDict = {}
            for i in range(0, len(userAll), 1):
                userDict[userAll[i].userName] = userAll[i].nickname

            userDict_json = json.dumps(userDict)

            context = {
                'postMsg': 'Post created',
                'nickname': user.nickname,
                'postPerPage': postPerPage,
                'pageNum': 1,
                'userDict': userDict_json,
                'allowDel': allowDel,
                # 'postMsg': errMsg
            }
            template = loader.get_template('postform.html')
            response = HttpResponse(template.render(context, request))

    return response


def getimgurl(request):
    serving_url = "No URL"
    if request.method == "GET":
        name = request.GET.get('name', 'default')
        client = storage.Client()  # Implicit environ set-up
        bucket = client.bucket('offerimage-may2018.appspot.com')
        blob = bucket.blob(name)
        expiration = timedelta(minutes=60)
        serving_url = blob.generate_signed_url(expiration, method="GET",)

    return JsonResponse({ "url": serving_url })

credential_path = os.path.join(settings.BASE_DIR, 'drinks', 'gcs_bucket.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def resize_image(image, max_length=1024):
    # Open the image with PIL
    img = Image.open(image)
    
    # Apply orientation from EXIF data, if available
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = img._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # If no EXIF data is found, skip orientation adjustment
        pass

    # Set the format if not detected
    format_ = img.format or 'JPEG'  # Use 'JPEG' or 'PNG' as a fallback

    # Calculate the new size, keeping the aspect ratio
    if img.width > img.height:
        new_width = max_length
        new_height = int((max_length / img.width) * img.height)
    else:
        new_height = max_length
        new_width = int((max_length / img.height) * img.width)
    
    # Resize the image using LANCZOS (high-quality resampling)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Save the resized image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format=format_)
    img_io.seek(0)

    # Create a new InMemoryUploadedFile object
    resized_image = InMemoryUploadedFile(
        img_io, 
        None,  # Replace field_name with None
        f"{image.name.split('.')[0]}.{format_.lower()}",  # set the correct extension
        image.content_type, 
        sys.getsizeof(img_io), 
        image.charset
    )
    
    return resized_image

def delPost(request):

    userName=request.session.get('userName')
    if userName and userName == "albert88hk@yahoo.com.hk":
        try:
            postId = int(request.GET.get('id', 0))
        except:
            postId = 0
        if postId > 0:
            try:
                post = Post.objects.get(pk=postId)
            except:
                post = None
            if post:
                if post.image and not post.image == "":
                    # Initialize a client
                    client = storage.Client()
                    # Get the bucket
                    bucket = client.get_bucket('offerimage-may2018.appspot.com')
                    # Get the blob (file) to delete
                    folder_name = 'images'
                    blob = bucket.blob(f'{folder_name}/{post.image}')
                    # Delete the blob
                    blob.delete()
                post.delete()

        template = loader.get_template('postform.html')
        userAll = User.objects.all()
        userDict = {}
        for i in range(0, len(userAll), 1):
            userDict[userAll[i].userName] = userAll[i].nickname

        userDict_json = json.dumps(userDict)

        user = User.objects.filter(userName=request.session.get('userName')).first()
        nickname = user.nickname

        try:
            pageNum = int(request.GET.get('pageNum', 0))
        except:
            pageNum = 0
        if pageNum > 0:
            allPost = Post.objects.all()
            totalPage = len(allPost) / postPerPage
            if pageNum > totalPage:
                pageNum = totalPage
        else:
            pageNum = 1

        context = {
            'placeholder': 'test',
            'nickname': nickname,
            'postPerPage': postPerPage,
            'pageNum': pageNum,
            'userDict': userDict_json,
            'allowDel': "Y",
        }
        response = HttpResponse(template.render(context, request))           
    else:      
        template = loader.get_template('login.html')
        context = {
                'placeholder': 'test',
        }
        response = HttpResponse(template.render(context, request))        

    return response


def csrf_failure(request, reason=""):
    
    user = User.objects.filter(userName=request.session.get('userName')).first()

    if user is None:
        nickname = None
    else:
        nickname = user.nickname

    context = {
        'page': 'registerForm',
        'registerMsg': 'CSRF verification failure, reason: ' + reason,
        'nickname': nickname,
    }
    template = loader.get_template('thank_register.html')
    response = HttpResponse(template.render(context, request)) 

    return response

def deliveryForm(request):

    userName = request.session.get('userName')

    if userName:    
        template = loader.get_template('deliveryForm.html')
        context = {
            'placeholder': 'test',
        }
        response = HttpResponse(template.render(context, request))   
    else:
        template = loader.get_template('login.html')
        context = {
            'errMsg': 'Please login to create a delivery'
        }
        response = HttpResponse(template.render(context, request))   

    return response

def deliveryAdd(request):
    
    userName = request.session.get('userName')

    if userName is None:
        template = loader.get_template('login.html')
        context = {
            'errMsg': 'Please login to create a delivery'
        }
        response = HttpResponse(template.render(context, request))
    else:
        if request.method == 'POST':    
            deliveryObj = Delivery.objects.create(
                        lastName = request.POST['lastname'],
                        firstName = request.POST['firstname'],
                        dateOfBirth = '01/01/2000',
                        deliveryDate = '01/01/2024',
                        address = '',
                        selfPickup = 'N',
                        parentID = 0,
                        repeatFreq = 'Monthly',
                        eligible = 'N',
                        ticketNo = 0,
                        leaveAtDoor = 'Y',
                        phoneForPic = '123-456-7890',
                        status = 'Planned',
                        log = '',
                        comments = None)
            deliveryObj.save()
            template = loader.get_template('deliveryForm.html')
            context = {
                'errMsg': 'A delivery is created'
            }
            response = HttpResponse(template.render(context, request))         
        else:
            template = loader.get_template('deliveryForm.html')
            context = {
                'errMsg': 'POST request is required to create a delivery'
            }
            response = HttpResponse(template.render(context, request))         

    return response   

def deliveryList(request):
    
    userName = request.session.get('userName')

    if userName:
        deliveryAll = Delivery.objects.all()
        deliveryArray = []
        for i in range(0, len(deliveryAll), 1):
            deliveryArray.append({
                "id": deliveryAll[i].id,
                "deliveryDate": deliveryAll[i].deliveryDate,
                "lastName": deliveryAll[i].lastName,
                "firstName": deliveryAll[i].firstName,
                                 })

        delivery_json = json.dumps(deliveryArray)

        template = loader.get_template('deliveryList.html')
        context = {
            'errMsg': 'Please login to create a delivery',
            'delivery_json': delivery_json,
        }
        response = HttpResponse(template.render(context, request))      
    else:
        template = loader.get_template('login.html')
        context = {
            'errMsg': 'Please login to create a delivery'
        }
        response = HttpResponse(template.render(context, request))        

    return response