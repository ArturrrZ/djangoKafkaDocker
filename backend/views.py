from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError  # to catch duplicate username
from django.http import HttpResponse
import os
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
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            file_path = os.path.join(folder_path, f'newUser_{email}.txt')
            print(file_path)
            with open(file_path, 'w') as file:
                file.write(f"Welcome {email} to our service!")
            return HttpResponse("Registration successful!")
        except IntegrityError:
            return HttpResponse("Username already taken.")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return render(request, 'accounts/register.html')
