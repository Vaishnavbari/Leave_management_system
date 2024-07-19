# from django 
from django.shortcuts import render, redirect

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from models and serializer
from .models import LeaveType, LeaveRule, Leave
from user_registration.models import Role 
from leaves.serializer import LeaveTypeSerializer, LeaveRuleSerializer, LeaveSerializer, LeaveApproveSerializer

# from jwt authorization and utils files 
from leave_management.jwt_authorization import JWTAuthorization, CheckPermission
from leave_management.renderers import UserRenderer
from leave_management.utils import handle_exceptions
from datetime import datetime
from leaves.paginations import CustomPagination


class LeaveTypeView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()
    def post(self, request):
        serializer = LeaveTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Leave type created successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
    
    @handle_exceptions()
    def put(self, request, id):

        leave_type_data = LeaveType.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not leave_type_data:
            return Response({"message":"Leave type not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeaveTypeSerializer(instance=leave_type_data.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Leave type updated successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_200_OK)
    
    @handle_exceptions()
    def delete(self, request, id):
        leave_type_data = LeaveType.objects.filter(id=id, deleted_at__isnull=True)
        if not leave_type_data:
            return Response({"message":"leave type not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_type_data.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Leave deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    
    # @handle_exceptions()
    def get(self, request, count=None):
        leaveData = LeaveType.objects.filter(deleted_at__isnull=True)
        if count is not None:
            return render(request, "leaves/leavedata.html", {"data": leaveData})
        return render(request, "leaves/createLeaves.html", {"data": leaveData})


class LeaveRuleView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    # @handle_exceptions()
    # def post(self, request):
    #     validity = request.data.getlist("validity[]")
    #     leave_type = request.data.get("leave_type")
    #     role = request.data.getlist("role[]")
    #     id = request.data.getlist("id[]")
    #     serializer = LeaveRuleSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"message":"Leave rule created successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)

    @handle_exceptions()
    def post(self, request):
        validity = request.data.getlist("validity[]")
        leave_type = request.data.get("leave_type")
        role = request.data.getlist("role[]")
        id = request.data.getlist("id[]")

        if not leave_type:
            return Response({"message":"Leave type is required", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        for index in range(len(role)):
            if not validity[index]:
                return Response({"message":"validity field is required", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
            if int(validity[index]) < 0:
                return Response({"message":"validity field should be greater than 0", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
            
        leave = LeaveType.objects.filter(id=leave_type).first()
        for index in range(len(role)):
            leave_rule = LeaveRule.objects.filter(leave_type=leave.id, role=id[index], deleted_at__isnull=True)
            if leave_rule.exists():
                return Response({"message":"Leave rule already exists", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        for index in range(len(role)):
            leave_rule = LeaveRule.objects.create(leave_type=leave, role=Role.objects.filter(id=id[index]).first(), validity=validity[index])

        return Response({"message":"Leave rule created successfully..!!", "status":"success"}, status=status.HTTP_201_CREATED)

    
    @handle_exceptions()
    def put(self, request, id):

        leave_rule_data = LeaveRule.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not leave_rule_data:
            return Response({"message":"Leave rule not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = LeaveRuleSerializer(instance=leave_rule_data.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Leave rule updated successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_200_OK)

    @handle_exceptions()                     
    def delete(self, request, id):
        leave_rule_data = LeaveRule.objects.filter(id=id, deleted_at__isnull=True)
        if not leave_rule_data:
            return Response({"message":"leave rule not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_rule_data.update(deleted_at=datetime.now(), deleted_by=request.user.id, validity=0)
        return Response({"message":"Leave rule deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    
    def get(self, request):
        leavedata = LeaveType.objects.filter(status=True, deleted_at__isnull=True)
        roledata = Role.objects.filter(status=True, deleted_at__isnull=True).exclude(name="admin")
        return render(request, "leaves/leaverule.html", {"data": leavedata, "roledata":roledata})

class LeaveView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization]
    
    # @handle_exceptions()
    def post(self, request):
        serializer = LeaveSerializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Leave applied successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
    
    # @handle_exceptions()
    # def put(self, request, id):

    #     leave_data = Leave.objects.filter(id=id, user=request.user.id, status=True)
    #     if not leave_data:
    #         return Response({"message":"Leave not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)      
        
    #     serializer = LeaveSerializer(instance=leave_data.first(), data=request.data, context={"user":request.user}, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"message":"Leave updated successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_200_OK)

    @handle_exceptions()                     
    def delete(self, request, id):
        leave_data = Leave.objects.filter(id=id, deleted_at__isnull=True, status="1")
        if not leave_data:
            return Response({"message":"Leave not found or already action perform on this leave", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_data.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Leave deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    
    # @handle_exceptions()  
    def get(self, request, count=None):
        leavetype_data = LeaveType.objects.filter(status=True, deleted_at__isnull=True)
        leave_data = Leave.objects.filter(deleted_at__isnull=True).order_by("-id")
        if count is not None:
            return render(request, "leaves/leaves.html",{"data": leave_data, "leavetype":leavetype_data})
        return render(request, "leaves/addleave.html",{"data": leave_data, "leavetype":leavetype_data})

    

class UpdateLeaveTypeStatus(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]

    @handle_exceptions()  
    def put(self, request, id):

        data = LeaveType.objects.filter(id=id, deleted_at__isnull=True)
        if not data:
            return Response({"message":"Leave Type not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if data.first().status:
            data.update(status=False)
        else:
            data.update(status=True)
        
        return Response({"message":"Status updated successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    

class UpdateRuleStatus(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
 
    @handle_exceptions()  
    def put(self, request, id):

        data = LeaveRule.objects.filter(id=id, deleted_at__isnull=True)
        if not data:
            return Response({"message":"Leave rule not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if data.first().status:
            data.update(status=False)
            return Response({"message":"Status updated successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
        else:
            data.update(status=True)
        
        return Response({"message":"Status updated successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    

class LeaveApprovedView(APIView):

    renderer_classes = [UserRenderer]
    # permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()  
    def put(self, request, id):

        leave_data = Leave.objects.filter(id=id)
        if not leave_data:
            return Response({"message":"Leave not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role.name == "Developer" and request.user.role.name == leave_data.first().user.role.name:
            return Response({"message":"You are not authorized to approve this leave", "status":"error"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = LeaveApproveSerializer(instance=leave_data.first(), data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Get leave status 
        status_keys = dict(Leave.select_status)
        status_name = status_keys.get(int(request.data.get("status")))

        return Response({"message":f"Leave {status_name} by {request.user.role.name}..!!", "data":LeaveSerializer(leave_data.first()).data, "status":"success"}, status=status.HTTP_200_OK)
    
    @handle_exceptions()  
    def get(self, request, count=None):

        leave_data = Leave.objects.filter(deleted_at__isnull=True).order_by("-id")
        if count is not None:
            return render(request, "leaves/leave_approval_table.html",{"data": leave_data})
    
        return render(request, "leaves/leave_approval.html",{"data": leave_data})


        

class LeaveRuleData(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]

    pagination_class = CustomPagination

    @handle_exceptions()  
    def get(self, request, counts=None):
        leave_rule_data = {}

        query = LeaveRule.objects.filter(deleted_at__isnull=True).order_by("created_at")

        for rule in query:
            leave_type_id = rule.leave_type.id
            if leave_type_id not in leave_rule_data:
                leave_rule_data[leave_type_id] = []

            leave_rule_data[leave_type_id].append({

                "id":rule.id,
                "leave_type_id":leave_type_id,
                "leave_type": rule.leave_type.type,
                "validity": rule.validity,
                "status": rule.status,
                "role": rule.role.name,
            })

        if counts is not None:
            return render(request, "leaves/leaveruletable.html", {"data": leave_rule_data})

        return render(request, "leaves/leaveruledata.html", {"data": leave_rule_data})
    

class UpdateLeaveRuleData(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()  
    def get(self, request, id):
        leave_rule_data = LeaveRule.objects.filter(leave_type_id=id)
        if not leave_rule_data:
            return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
        return render(request, "leaves/editleaverule.html", {"data":leave_rule_data})
    
    # @handle_exceptions()   
    def post(self, request):
        validity = request.data.getlist("validity[]")
        leave_type = request.data.get("leave_type")
        role_id = request.data.getlist("id[]")
        rule_id = request.data.getlist("rule[]")
        
        for index in range(len(role_id)):
            if not validity[index]:
                return Response({"message":"validity field is required", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
            if int(validity[index]) < 0:
                return Response({"message":"validity field should be greater than 0", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
            
        for index, id in enumerate(rule_id, start=0):
            leave_rule_data = LeaveRule.objects.filter(id=id).first()
            leave_rule_data.validity = validity[index]
            leave_rule_data.leave_type = LeaveType.objects.filter(id=leave_type).first()
            leave_rule_data.role = Role.objects.filter(id=int(role_id[index])).first()
            leave_rule_data.deleted_at=None
            leave_rule_data.save()

        return Response({"message":"success", "status":"success"}, status=status.HTTP_200_OK)
        # return redirect("LeaveRuleData")




    
    



