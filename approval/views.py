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
    Comment,
    Notification,
)

from .utils import workflow_decider,approval_forwarder,staff_count
# Create your views here.

User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        profile = User_profile.objects.get(User = request.user.id)
        notifications = Notification.objects.filter(user = profile)
        return render(request, 'home.html',{'profile':profile,'notifications':notifications})
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

def company(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        companys = Company.objects.exclude(name = 'main').order_by('name')
        return render(request,'company.html',{'companys':companys,'profile':user})
    return redirect('/login/')

def remove_company(request,obj_id):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        company = Company.objects.get(id = obj_id)
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
        staff = User_profile.objects.filter(role = 'staff')
        workflows = Workflow.objects.all().order_by('name')
        worksteps = WorkflowStep.objects.all().order_by('sequence')
        return render(request,'workflow.html',{'workflows':workflows,'profile':user,'worksteps':worksteps,'staff':staff})
    return redirect('/login/')

import json

def workflow_create(request):
    '''form = WorkflowForm(request.POST or None)
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
    return render(request,'workflow_create.html',{'form':form})'''

    form = WorkflowForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        threshold_value = form.cleaned_data.get('threshold_value')
        staff_users = User_profile.objects.filter(role='staff')
        staffs = dict()
        sequence = {}
        for user in staff_users:
            staffs[user.id] = user.User.first_name
        for id in staffs.keys():
            sequence[id] = form.cleaned_data.get(staffs[id])

        user_sequence = {}
        for key, value in sequence.items():
            user_sequence.setdefault(value, []).append(key)

        workflow_obj = Workflow.objects.create(name = name, description = description, threshold_value = threshold_value)
        workflow_obj.save()
        print(user_sequence)
        for key in user_sequence.keys():
            users = { 'user_id': user_sequence[key] }
            
            obj = WorkflowStep.objects.create(
                workflow = workflow_obj,
                sequence = int(key),
                users = users,
            )
            obj.save()
        return redirect('/workflow/')
    return render(request,'workflow_create.html',{'form':form})

def delete_workflow(request,obj_id):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated and user.role == 'admin':
        workflow = Workflow.objects.get(id = obj_id)
        if workflow:
            workflow.delete()
            return redirect('/workflow/')
        return HttpResponse('Company with that id does not exist')
    return redirect('/login/')



def approval(request):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated:
        comments = Comment.objects.all()
        if user.role == 'admin' :
            approvals = Approval.objects.all()
            approval_objs = []
            header_line = list()
            for approval in approvals:
                header_line.append(approval.header_detail)
            header_line = set(header_line)
            for header in header_line:
                obj = Approval.objects.filter(header_detail = header,status = 'approved').order_by('sequence').reverse().first()
                if obj:
                    approval_objs.append(obj)
                else:
                    obj = Approval.objects.filter(header_detail = header,).order_by('sequence').reverse().first()
                    approval_objs.append(obj)
        if user.role == 'staff':
            '''worksteps = WorkflowStep.objects.filter(user = user.id)
            workstep_ids = worksteps.values_list('id',flat=True)
            approval_objs = []
            approvals  = Approval.objects.filter(workflowstep__in = workstep_ids,status = 'pending')
            for approval in approvals:
                obj = Approval.objects.filter(header_detail = approval.header_detail,status = 'pending').order_by('id').reverse().first()
                approval_objs.append(obj)
                    
            return render(request,'approvals.html',{'approvals':approval_objs,'profile':user,'comments':comments})'''

            

            workflowsteps = WorkflowStep.objects.all()
            workflowsteps_ids = []
            for obj in workflowsteps:
                user_dict = obj.users['user_id']
                if user.id in user_dict:
                    workflowsteps_ids.append(obj.id)

            approval_objs = Approval.objects.filter(workflowstep__in = workflowsteps_ids,status = 'pending' )
            approval_ids = [obj.id for obj in approval_objs]
            comments = Comment.objects.filter(approval__in = approval_ids)
            return render(request,'approvals.html',{'approvals':approval_objs,'profile':user,'comments':comments})

        else:
            #approvals = Approval.objects.filter(creator = user.id)
            approvals = Approval.objects.filter(creator=user.id)
            '''approval_objs = []
            header_line = list()
            for approval in approvals:
                header_line.append(approval.header_detail)
            header_line = set(header_line)
            for header in header_line:
                obj = Approval.objects.filter(header_detail = header).order_by('id').reverse().first()
                approval_objs.append(obj)'''
            
            return render(request,'approvals.html',{'approvals':approvals,'profile':user,'comments':comments})
        
            


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

            #workflow_ids = workflow_decider()

            #edited 

            workflow_id = workflow_decider()

            '''for id  in workflow_ids:
                workflow = WorkflowStep.objects.get(id = id)
                obj = Approval.objects.create(
                    header_detail = header,
                    line_item_detail = line_items,
                    status =  status,
                    approval_type = approval_type,
                    creator = creator,
                    workflowstep = workflow, # workflowstep object
                    sequence = workflow.sequence,
                )
                obj.save()
                text = f'An approval has been forwarded to you by {user.User.first_name}'
                notification = Notification.objects.create(
                    text = text,
                    user = workflow.user,
                )
                notification.save()
            '''

            workflowstep_obj = WorkflowStep.objects.filter(id = workflow_id ).first()

            if workflowstep_obj:
                obj = Approval.objects.create(
                    header_detail = header,
                    line_item_detail = line_items,
                    status =  status,
                    approval_type = approval_type,
                    creator = creator,
                    workflowstep = workflowstep_obj, # workflowstep object
                    sequence = workflowstep_obj.sequence,
                )
                obj.save()
                text = f'An approval has been forwarded to you by {user.User.first_name}'

                obj_ids = workflowstep_obj.users['user_id']
                for obj_id in obj_ids:
                    u_obj = User_profile.objects.get(id=obj_id)
                    notification = Notification.objects.create(
                        text = text,
                        user = u_obj,
                    )
                    notification.save()


                return redirect('/approval/')
            
        return render(request,'approval_create.html',{'form':form,'profile':user})
    return redirect('/login/')


def approval_delete(request,obj_id):
    if request.user.is_authenticated:
        approval = Approval.objects.filter(id =obj_id).first()
        if approval:
            approvals = Approval.objects.filter(header_detail = approval.header_detail)
            for obj in approvals:
                obj.delete()
            return redirect('/approval/')
        return HttpResponse('NO approval found')
    return redirect('/login/')


def comment_create(request,obj_id):
    user_obj = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated:
        comments = Comment.objects.all()
        if request.method == 'POST':
            comment = request.POST.get('comment')
            approval = Approval.objects.get(id = obj_id)
            user = user_obj

            obj = Comment.objects.create(
                text = comment,
                approval = approval,
                user = user,
            )
            obj.save()

            return redirect('/approval/')
        return redirect('/approval/')
    return redirect('/login/')



def approval_approve(request,obj_id):
    user = User_profile.objects.get(User = request.user.id)
    if request.user.is_authenticated:
        approval = Approval.objects.get(id = obj_id)
        if approval:
            result = approval_forwarder(approval_id=approval.id,workflowstep_id=approval.workflowstep.id,user_id = user.id)
            if result == 'forwarded':
                return redirect('/approval/')
            else:
                text = f"Your approval:{approval.header_detail[:5]} has been approved"
                notification = Notification.objects.create(
                    text = text,
                    user = approval.creator,
                )
                notification.save()
                approval.status = 'approved'
                approval.save()
                return redirect('/approval/')
        return HttpResponse('Invalid approval id provided.')
    return redirect('/login/')

def approval_reject(request,obj_id):
    # user = User_profile.objects.get(User = request.user.id)
    # count = staff_count()
    if request.user.is_authenticated:
        approval = Approval.objects.get(id = obj_id)
        if approval:
            approval.status = 'rejected'
            '''approvals = Approval.objects.filter(header_detail = approval.header_detail).exclude(status = 'rejected')
            approvals.delete()
            approval.sequence = count+10'''
            approval.save()
            text = f"Your approval:{approval.header_detail[:5]} has been rejected"
            notification = Notification.objects.create(
                text = text,
                user = approval.creator,
            )
            notification.save()
            return redirect('/approval/')
        return HttpResponse('Invalid approval id provided.')
    return redirect('/login/')


@login_required
def notification_remove(request,obj_id):
    notification = Notification.objects.filter(id = obj_id).first()
    if notification:
        notification.delete()
        return redirect('/')
    return redirect('/')
