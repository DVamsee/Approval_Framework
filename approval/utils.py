from .models import (
    User_profile,
    Company,
    Workflow,
    WorkflowStep,
    Approval,
)


def workflow_decider():
    approval_count = 500
    #approval_count = Approval.objects.filter(approval_type = 'pending').count()
    workflows = Workflow.objects.order_by('threshold_value').reverse()
    workstep_ids = []
    for workflow in workflows:
        threshold_value = workflow.threshold_value

        if approval_count > threshold_value:
            workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
            worksteps = WorkflowStep.objects.filter(sequence = workstep.sequence,workflow = workflow.id)
            for obj in worksteps:
                workstep_ids.append(obj.id)
            return workstep_ids
    else:
        workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
        worksteps = WorkflowStep.objects.filter(sequence = workstep.sequence,workflow = workflow.id)
        for obj in worksteps:
            workstep_ids.append(obj.id)
        return workstep_ids
    
from django.db import transaction

def approval_forwarder(approval_id, workflowstep_id):
    approval = Approval.objects.get(id=approval_id)
    workstep = WorkflowStep.objects.get(id=workflowstep_id)

    # Find next WorkflowStep(s) with the same sequence within the same workflow
    next_worksteps = WorkflowStep.objects.filter(sequence=workstep.sequence+1, workflow=workstep.workflow).order_by('sequence')
    count = len(next_worksteps)

    if next_worksteps.exists():
        with transaction.atomic():
            x = 0
            for next_workstep in next_worksteps:
                approval_obj = Approval.objects.create(
                    header_detail=approval.header_detail,
                    line_item_detail=approval.line_item_detail,
                    status=approval.status,
                    approval_type=approval.approval_type,
                    creator=approval.creator,
                    workflowstep=next_workstep,
                )
                approval_obj.save()
                x+=1

            # Update the original approval to the latest WorkflowStep
            worksteps = WorkflowStep.objects.filter(sequence = workstep.sequence, workflow=workstep.workflow)
            workstep_ids = worksteps.values_list('id',flat=True)

            approvals =[]
            for ids in workstep_ids:
                workstep = WorkflowStep.objects.get(id = ids)
                obj = Approval.objects.get(
                workflowstep = workstep.id,
                header_detail=approval.header_detail,
                line_item_detail=approval.line_item_detail,
                creator=approval.creator.id,
                )
                obj.workflowstep = next_worksteps.first()
                obj.delete()

            return 'forwarded'
    else:
        return 'approved'

    

