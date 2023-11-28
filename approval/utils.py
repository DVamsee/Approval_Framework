from .models import (
    User_profile,
    Company,
    Workflow,
    WorkflowStep,
    Approval,
    Comment,
    Notification,
)

def staff_count():
    return User_profile.objects.all().count()

def workflow_decider():
    
    approval_count = Approval.objects.filter(approval_type = 'pending').count()
    workflows = Workflow.objects.order_by('threshold_value').reverse()
    workstep_ids = []
    for workflow in workflows:
        threshold_value = workflow.threshold_value

        if approval_count > threshold_value:
            workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
            worksteps = WorkflowStep.objects.filter(sequence = workstep.sequence,workflow = workflow.id)
            '''for obj in worksteps:
                workstep_ids.append(obj.id)
            return workstep_ids'''

            #edited
            return int(workstep.id)
    else:
        workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
        worksteps = WorkflowStep.objects.filter(sequence = workstep.sequence,workflow = workflow.id)
        '''for obj in worksteps:
            workstep_ids.append(obj.id)
        return workstep_ids'''

            #edited
        return int(workstep.id)
    
from django.db import transaction

def approval_forwarder(approval_id, workflowstep_id,user_id):
    # approval = Approval.objects.get(id=approval_id)
    # workstep = WorkflowStep.objects.get(id=workflowstep_id)

    # # Find next WorkflowStep(s) with the same sequence within the same workflow

    # #edited the greater than  in the filter function
    # next_workstep = WorkflowStep.objects.filter(sequence=workstep.sequence+1, workflow=workstep.workflow).first()

    # #if next_worksteps.exists():

    # if next_workstep:
    #     #with transaction.atomic():    edited 
    #     '''for next_workstep in next_worksteps:
    #             approval_obj = Approval.objects.create(
    #             header_detail=approval.header_detail,
    #             line_item_detail=approval.line_item_detail,
    #             status=approval.status,
    #             approval_type=approval.approval_type,
    #             creator=approval.creator,
    #             workflowstep=next_workstep,
    #             sequence = next_workstep.sequence,
    #         )'''
            
    #     approval.sequence = next_workstep.sequence
    #     approval.workflowstep = next_workstep

    #     text = f'An approval has been forwarded to you by {workstep.user.User.first_name}'
    #     notification = Notification.objects.create(
    #         text = text,
    #         user = next_workstep.user,
    #     )
    #     approval.save()
    #     notification.save()
        
    #     '''comments = Comment.objects.filter(approval = approval.id)
    #     for comment in comments:
    #         comment.approval = approval_obj
    #         comment.save()'''

    #     return 'forwarded'
    # else:

    #     return 'approved'
    approver = User_profile.objects.get(id = user_id)
    approval = Approval.objects.filter(id = approval_id).first()
    if approval:
        workflowstep = WorkflowStep.objects.filter(approval = approval.id).first()
        next_steps = WorkflowStep.objects.filter(workflow = workflowstep.workflow.id,sequence__gt = workflowstep.sequence).order_by('sequence').first()
        next_step_id = next_steps.id if next_steps else None
        # print(f'WorkflowStep Sequence: {workflowstep.sequence}')
        # print(f'Next Step Sequence: {next_step.sequence if next_step else None}')
        if next_step_id:
            next_step = WorkflowStep.objects.filter(id = next_step_id).first()
            approval.sequence = next_step.sequence
            approval.workflowstep = next_step
            approval.save()
            user_objs = next_step.users['user_id']
            for user_id in user_objs:
                user = User_profile.objects.get(id = user_id)    
                text = f'An approval has been forwarded to you by {approver.User.first_name}'
                notification = Notification.objects.create(
                text = text,
                user = user,
        
                )
                notification.save()
            
            return 'forwarded'
        
        else:
            return 'approved'
