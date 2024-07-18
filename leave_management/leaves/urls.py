from django.urls import path
from . import views

urlpatterns = [
    # LeaveType
    path("add", views.LeaveTypeView.as_view(), name="AddLeaveType"),
    path("add/<int:count>", views.LeaveTypeView.as_view(), name="AddLeaveTypes"),

    path("update/<int:id>", views.LeaveTypeView.as_view(), name="UpdateLeaveType"),
    path("delete/<int:id>", views.LeaveTypeView.as_view(), name="DeleteLeaveType"),

     # LeaveRule
    path("add/leave/rule", views.LeaveRuleView.as_view(), name="AddLeaveRule"),
    path("update/leave/rule/<int:id>", views.LeaveRuleView.as_view(), name="UpdateLeaveRule"),
    path("delete/leave/rule/<int:id>", views.LeaveRuleView.as_view(), name="DeleteLeaveRule"),

    # Leave
    path("add/user-leave", views.LeaveView.as_view(), name="AddLeave"),
     path("add/user-leave/<int:count>", views.LeaveView.as_view(), name="LeaveTable"),
    # path("update/user-leave/<int:id>", views.LeaveView.as_view(), name="Update"),
    path("delete/user-leave/<int:id>", views.LeaveView.as_view(), name="DeleteLeave"),

    #  Update status 
    path("update/leave-rule-status/<int:id>", views.UpdateRuleStatus.as_view(), name="UpdateLiveRuleStatus"),
    path("update/leave-type-status/<int:id>", views.UpdateLeaveTypeStatus.as_view(), name="UpdateLiveTypeStatus"),
    
    # Leave approved by 
    path("approve/update", views.LeaveApprovedView.as_view(), name="ApproVal-Page"),
    path("approve/update/<int:count>", views.LeaveApprovedView.as_view(), name="Approved"),
    path("approve/<int:id>", views.LeaveApprovedView.as_view(), name="ApproVal"),

    #Leave rule data  
    path("leave-rule-data", views.LeaveRuleData.as_view(), name="LeaveRuleData"),
    path("leave-rule-data/<int:counts>", views.LeaveRuleData.as_view(), name="LeaveRuleDataTable"),

    # edit leave rule data 
    path("edit-leave-rule-data/<int:id>", views.UpdateLeaveRuleData.as_view(),name="EditLeaveRuleData"),
    path("update-leave-rule-data", views.UpdateLeaveRuleData.as_view(),name="UpdateLeaveRuleDataTable"),
]