import numpy as np
import joblib
import os
import re

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



model = joblib.load('app1/trained_model.pkl')



# Encoding functions
def encode_owner(owner):
    if owner == 'First Owner':
        return [1.0, 0.0, 0.0]
    elif owner == 'Second Owner':
        return [0.0, 1.0, 0.0]
    elif owner == 'Third Owner':
        return [0.0, 0.0, 1.0]
    else:
        raise ValueError("Invalid owner type. Choose from 'First', 'Second', or 'Third'.")

def encode_fuel_type(fuel_type):
    if fuel_type == 'Petrol':
        return 1
    elif fuel_type == 'Diesel':
        return 0
    else:
        raise ValueError("Invalid fuel type. Choose 'Petrol' or 'Diesel'.")

def encode_deal_type(deal_type):
    if deal_type == 'Individual':
        return 1
    elif deal_type == 'Dealer':
        return 0
    else:
        raise ValueError("Invalid deal type. Choose 'Individual' or 'Dealer'.")

def encode_transmission_type(transmission_type):
    if transmission_type == 'Manual':
        return 1
    elif transmission_type == 'Automatic':
        return 0
    else:
        raise ValueError("Invalid transmission type. Choose 'Manual' or 'Automatic'.")

# CSRF exempt for simplicity, but not recommended in production
@csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        try:
            # Receive data from the form
            owner_type = request.POST.get('owner')
            fuel_type = request.POST.get('fuel_type')
            deal_type = request.POST.get('deal')
            transmission_type = request.POST.get('transmission')
            year = int(request.POST.get('year'))
            mileage = float(request.POST.get('mileage'))
            engine_size = float(request.POST.get('engine_size'))
            power = float(request.POST.get('power'))
            seats = float(request.POST.get('seats'))
            kilometer_driven = float(request.POST.get('km_driven'))

            # Encode categorical values
            owner = encode_owner(owner_type)
            fuel = encode_fuel_type(fuel_type)
            deal = encode_deal_type(deal_type)
            transmission = encode_transmission_type(transmission_type)

            # Combine all features
            input_features = owner + [year, kilometer_driven, fuel, deal, transmission, power, mileage, engine_size, seats]
            
            # Make prediction in INR
            predicted_price_inr = model.predict([input_features])[0]

            # Convert to Nepali Rupees (NPR)
            conversion_rate = 1.6  # 1 INR = 1.6 NPR (you can update this rate)
            predicted_price_npr = predicted_price_inr * conversion_rate

            # Render the 'master.html' with prediction in NPR
            return render(request, 'master.html', {'prediction': round(predicted_price_npr, 2)})
        
        except Exception as e:
            # Handle error and display it on the page
            return render(request, 'master.html', {'error': str(e)})
    
    # If the request method is not POST, render the form without prediction
    return render(request, 'master.html')

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        context = {
            'username': uname,
            'email': email,
        }

        # Validate username
        if not re.match(r'^[a-zA-Z0-9]+$', uname):
            context['error'] = 'Username can only contain letters and numbers!'
            return render(request, 'signup.html', context)

        # Check if passwords match
        if pass1 != pass2:
            context['error'] = 'Passwords do not match!'
            return render(request, 'signup.html', context)

        # Check password length (at least 8 characters)
        if len(pass1) < 8:
            context['error'] = 'Password must be at least 8 characters long!'
            return render(request, 'signup.html', context)

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            context['error'] = 'Username already exists!'
            return render(request, 'signup.html', context)

        # Check if email is valid using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            context['error'] = 'Invalid email format!'
            return render(request, 'signup.html', context)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            context['error'] = 'Email already exists!'
            return render(request, 'signup.html', context)

        # If validation passes, create the user
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'error': 'Username or password is incorrect!'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def master_view(request):
    # You can add any logic here if needed
    return render(request, 'master.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


