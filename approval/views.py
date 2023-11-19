from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm
from django.http import HttpResponse
import datetime
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import (
    User_profile,
    Company,
)
# Create your views here.

User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        profile = User_profile.objects.get(User = request.user.id)
        return render(request, 'home.html',{'profile':profile})
    return render(request,'home.html')

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        company = form.cleaned_data.get('company')
        company_obj = Company.objects.get(name=company)
        password = form.cleaned_data.get('password')
        role = 'staff' if  company == 'stockone' else 'client'
        api_key = urlsafe_base64_encode(force_bytes(f'{first_name}{last_name}{email}{datetime.datetime.now()}'))

        user = User.objects.create(first_name = first_name,last_name = last_name,email = email, username = email, password = password)
        user.save()
        profile = User_profile.objects.create(User = user, role = role, company = company_obj,api_key = api_key)
        profile.save()


        
        return HttpResponse(api_key)
    return render(request,'registration.html',{'form':form})


def login(request):
    form = LoginForm(request.POST or None )
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username = username,password=password)
        if user != None:
            auth.login(request,user)
            return redirect('/')
    return render(request, 'login.html',{'form':form})


def profile(request):
    if request.user.is_authenticated:
        profile = User_profile.objects.get(User = request.user.id)
        return render(request, 'profile.html',{'profile':profile})
    return redirect('/login/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def approval(request):
    pass