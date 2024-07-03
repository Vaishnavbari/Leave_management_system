# from django 
from django.shortcuts import render

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# from models and serializer
from .models import LeaveType
from leaves.serializer import LeaveTypeSerializer

# from jwt authorization and utils files 
from leave_management.jwt_authorization import JWTAuthorization

class LeaveTypeView(APIView):

    authentication_classes = [JWTAuthorization]

    