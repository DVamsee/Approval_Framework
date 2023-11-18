from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class User_profile(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    role_choices = {
        ('admin', 'admin'),
        ('staff', 'staff'),
        ('client','client'),
    }
    role = models.CharField(max_length=50,choices=role_choices)
    api_key = models.CharField(max_length=50,default=None,null=True)
    def __str__(self):
        return self.User.first_name+" "+self.User.last_name
    
class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    threshold_value = models.IntegerField()  # Approval value threshold to trigger this workflow

    def __str__(self):
        return self.name

class WorkflowStep(models.Model):
    id = models.AutoField(primary_key=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    sequence = models.IntegerField() 

    def __str__(self):
        return f'{self.workflow.name}_{self.sequence}'

class Approval(models.Model):
    id = models.AutoField(primary_key=True)
    header_detail = models.TextField()
    line_item_detail = models.TextField()
    status_choices = {
        ('pending', 'Pending'),
          ('approved', 'Approved'), 
          ('rejected', 'Rejected'),
    }
    status = models.CharField(max_length=20, choices=status_choices)
    aprroval_choices = {
        ('urgent','urgent'),
        ('small','small'),
        ('adhoc','adhoc'),
    }
    approval_type = models.CharField(max_length=20,choices = aprroval_choices)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    creator = models.ForeignKey(User_profile, on_delete=models.CASCADE, related_name='created_approvals')

    def __str__(self):
        return self.id

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.id
    