from django.shortcuts import render
from .forms import RegistrationForm
from django.http import HttpResponse

# Create your views here.

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('first_name')
        return HttpResponse(f'{name}')
    return render(request,'registration.html',{'form':form})