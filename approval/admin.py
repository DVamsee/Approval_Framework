from django.contrib import admin
from .models import (
    User_profile,
    Approval,
    Workflow,
    WorkflowStep,
    Comment,
    Company,
    Notification,

)
# Register your models here.

admin.site.register(Company)
admin.site.register(User_profile)
admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(Approval)
admin.site.register(Comment)
admin.site.register(Notification)

