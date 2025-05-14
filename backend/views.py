from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError  # to catch duplicate username
from django.http import HttpResponse
import os
from kafka import KafkaProducer
import json
import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

folder_path = 'newusers'
os.makedirs(folder_path, exist_ok=True)

# Create your views here.
def home(request):
    return render(request, 'backend/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not username or not password or not email:
            return HttpResponse("All fields are required.")
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            now = datetime.datetime.now()
            joined = now.strftime("%Y-%m-%d")
            data = {"event":"user registration", "user": {
                "username": username,
                "email": email,
                "joined": joined 
            }}
            print(data)
            producer.send('registration', data)
            producer.flush()
            return HttpResponse("Registration successful!")
        except IntegrityError:
            return HttpResponse("Username already taken.")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return render(request, 'accounts/register.html')
