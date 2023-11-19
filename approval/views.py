from django.shortcuts import render,redirect
from .forms import (
    RegistrationForm,
    LoginForm,
    CompanyForm,
    WorkflowForm,
    ApprovalForm,
)
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
    Workflow,
    WorkflowStep,
    Approval,
)

from .utils import workflow_decider,approval_forwarder
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
        role = 'staff' if  company == 'main' else 'client'
        api_key = urlsafe_base64_encode(force_bytes(f'{first_name}{last_name}{email}{datetime.datetime.now()}'))

        user = User.objects.create(first_name = first_name,last_name = last_name,email = email, username = email, password = password)
        user.save()
        profile = User_profile.objects.create(User = user, password = password, role = role, company = company_obj,api_key = api_key)
        profile.save()


       
        return redirect('/login/')
    return render(request,'registration.html',{'form':form})


def login(request):
    form = LoginForm(request.POST or None )
    if form.is_valid():
        user = User.objects.get(username = form.cleaned_data.get('email'))
        auth.login(request,user)
        return render(request,'home.html')
    return render(request, 'login.html',{'form':form})


def profile(request):
    if request.user.is_authenticated:
        profile = User_profile.objects.get(User = request.user.id)
        return render(request, 'profile.html',{'profile':profile})
    return redirect('/login/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def company(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        companys = Company.objects.exclude(name = 'main').order_by('name')
        return render(request,'company.html',{'companys':companys,'profile':user})
    return redirect('/login/')

def remove_company(request,id):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        company = Company.objects.get(id = id)
        if company:
            company.delete()
            return redirect('/company/')
        return HttpResponse('Company with that id does not exist')
    return redirect('/login/')

def company_create(request):
    form = CompanyForm(request.POST or None)
    user = User_profile.objects.get(User = request.user.id)
    if user.role == 'admin':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            place = form.cleaned_data.get('place')
            obj = Company.objects.create(name = name,place = place)
            obj.save()

            return redirect('/company/')
        return render(request,'company_create.html',{'form':form})
    

def workflow(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin' :
        workflows = Workflow.objects.all().order_by('name')
        worksteps = WorkflowStep.objects.all().order_by('workflow')
        return render(request,'workflow.html',{'workflows':workflows,'profile':user,'worksteps':worksteps})
    return redirect('/login/')

def workflow_create(request):
    form = WorkflowForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        threshold_value = form.cleaned_data.get('threshold_value')
        staff_users = User_profile.objects.filter(role='staff')
        staffs = dict()
        sequence = dict()
        for user in staff_users:
            staffs[user.id] = user.User.first_name
        for id in staffs.keys():
            sequence[id] = form.cleaned_data.get(staffs[id])

        workflow_obj = Workflow.objects.create(name = name, description = description, threshold_value = threshold_value)
        workflow_obj.save()
        print(sequence)
        for id in sequence.keys():
            user = User_profile.objects.get(id = id)
            workstep_obj = WorkflowStep.objects.create(workflow = workflow_obj,user = user,sequence= sequence[id])
            workstep_obj.save()
        return redirect('/workflow/')
    return render(request,'workflow_create.html',{'form':form})

def delete_workflow(request,id):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        workflow = Workflow.objects.get(id = id)
        if workflow:
            workflow.delete()
            return redirect('/workflow/')
        return HttpResponse('Company with that id does not exist')
    return redirect('/login/')



def approval(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin' :
        approvals = Approval.objects.all()
        return render(request,'approvals.html',{'approvals':approvals,'profile':user})
    return redirect('/login/')

def approval_create(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated:
        form = ApprovalForm(request.POST or None)
        if form.is_valid():
            header = form.cleaned_data.get('header_detail')
            line_items = form.cleaned_data.get('line_item_detail')
            approval_type = form.cleaned_data.get('approval_type')
            status = 'pending'
            creator = user

            workflow_id = workflow_decider()
            workflow = WorkflowStep.objects.get(id = workflow_id)

            obj = Approval.objects.create(
                header_detail = header,
                line_item_detail = line_items,
                status =  status,
                approval_type = approval_type,
                creator = creator,
                workflowstep = workflow, # workflowstep object
            )
            obj.save()
            
            return redirect('/approval/')
            
        return render(request,'approval_create.html',{'form':form,'profile':user})
    return redirect('/login/')