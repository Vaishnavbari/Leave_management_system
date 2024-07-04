from django.db import models
from user_registration.models import Role, User

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


class LeaveRule(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    validity = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="LeaveRuleDeletedBy") 

    def __str__(self) -> str:
        return self.leave_type.type


class Leave(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LeaveAppliedBy")
    date_from = models.DateField()
    date_to = models.DateField()
    reason = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="LeaveDeletedBy")  

    def __str__(self) -> str:
        return self.user.username