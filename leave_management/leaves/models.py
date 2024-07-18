from django.db import models
from user_registration.models import Role, User
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin

# Create your models here.

class LeaveType(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="LeaveTypeDeletedBy") 

    def __str__(self):
        return self.type


class LeaveRuleQuerySet(QuerySet, GroupByMixin):
    pass


class LeaveRule(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    validity = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="LeaveRuleDeletedBy") 
    
    objects = LeaveRuleQuerySet.as_manager()

    def __str__(self) -> str:
        return self.leave_type.type


class Leave(models.Model):
    select_status = (
                    (1, 'Pending'),
                    (2, 'Approved'),
                    (3, 'Rejected'),
                   )

    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LeaveAppliedBy")
    date_from = models.DateField()
    date_to = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=select_status, default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="LeaveDeletedBy")
    approved_by_TL = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ApproveByTL")
    approved_by_HR = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ApproveByHR")
    approved_by_PM = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ApproveByPM")
    TL_status = models.CharField(max_length=50, choices=select_status, default=select_status[0][0])
    HR_status = models.CharField(max_length=50, choices=select_status, default=select_status[0][0])
    PM_status = models.CharField(max_length=50, choices=select_status, default=select_status[0][0])

    def __str__(self) -> str:
        return self.user.username
    
    def get_status_display(self):
        status_dict = dict(self.select_status)
        return status_dict[int(self.status)]

    def get_HR_status_display(self):
        status_dict = dict(self.select_status)
        return status_dict[int(self.HR_status)]
    
    def get_PM_status_display(self):
        status_dict = dict(self.select_status)
        return status_dict[int(self.PM_status)]
    
    def get_TL_status_display(self):
        status_dict = dict(self.select_status)
        return status_dict[int(self.TL_status)]
    

    

    
