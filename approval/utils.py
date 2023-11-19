from .models import (
    User_profile,
    Company,
    Workflow,
    WorkflowStep,
    Approval,
)


def workflow_decider():
    approval_count = Approval.objects.filter(approval_type = 'pending').count()
    workflows = Workflow.objects.order_by('threshold_value').reverse()

    for workflow in workflows:
        threshold_value = workflow.threshold_value

        if approval_count > threshold_value:
            workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
            return workstep.id
    else:
        workstep = WorkflowStep.objects.filter(workflow = workflow.id).order_by('sequence').first()
        return workstep.id
    

def approval_forwarder(approval_id, workflowstep_id):
    approval = Approval.objects.get(id=approval_id)
    workstep = WorkflowStep.objects.get(id=workflowstep_id)
    next_workstep = WorkflowStep.objects.filter(sequence__gt = workstep.sequence, workflow = workstep.workflow.id).order_by('sequence').first()
    if next_workstep:
        approval.workflowstep = next_workstep
        approval.save()

    

