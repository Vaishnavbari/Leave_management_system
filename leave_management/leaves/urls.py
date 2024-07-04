from django.urls import path
from . import views

urlpatterns = [
    # LeaveType
    path("add", views.LeaveTypeView.as_view(), name="AddLeaveType"),
    path("update/<int:id>", views.LeaveTypeView.as_view(), name="UpdateLeaveType"),
    path("delete/<int:id>", views.LeaveTypeView.as_view(), name="DeleteLeaveType"),
     # LeaveRule
    path("add/leave/rule", views.LeaveRuleView.as_view(), name="AddLeaveRule"),
    path("update/leave/rule/<int:id>", views.LeaveRuleView.as_view(), name="UpdateLeaveRule"),
    path("delete/leave/rule/<int:id>", views.LeaveRuleView.as_view(), name="DeleteLeaveRule"),
    # Leave
    path("add/user-leave", views.LeaveView.as_view(), name="AddLeave"),
    path("update/user-leave/<int:id>", views.LeaveView.as_view(), name="Update"),
    path("delete/user-leave/<int:id>", views.LeaveView.as_view(), name="DeleteLeave")
]