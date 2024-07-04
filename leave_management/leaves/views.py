# from django 
from django.shortcuts import render

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# from models and serializer
from .models import LeaveType, LeaveRule, Leave
from leaves.serializer import LeaveTypeSerializer, LeaveRuleSerializer, LeaveSerializer

# from jwt authorization and utils files 
from leave_management.jwt_authorization import JWTAuthorization, CheckPermission
from leave_management.renderers import UserRenderer
from leave_management.utils import handle_exceptions
from datetime import datetime


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
        leave_type_data = LeaveType.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not leave_type_data:
            return Response({"message":"leave type not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_type_data.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Leave deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    

class LeaveRuleView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()
    def post(self, request):
        serializer = LeaveRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Leave rule created successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
    
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
        leave_rule_data = LeaveRule.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not leave_rule_data:
            return Response({"message":"leave rule not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_rule_data.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Leave rule deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    

class LeaveView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization]

    
    @handle_exceptions()
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
        leave_data = Leave.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not leave_data:
            return Response({"message":"Leave not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        leave_data.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Leave deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
    

class UpdateLeaveTypeStatus(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]

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

    def put(self, request, id):

        data = LeaveRule.objects.filter(id=id, deleted_at__isnull=True)
        if not data:
            return Response({"message":"Leave rule not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if data.first().status:
            data.update(status=False)
        else:
            data.update(status=True)
        
        return Response({"message":"Status updated successfully..!!", "status":"success"}, status=status.HTTP_200_OK)