# from django 
from django.shortcuts import render
from django.contrib.auth import login, authenticate

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# from models and serializer
from .models import User, Token, Role
from user_registration.serializer import UserRegistrationSerializer, LoginSerializer, TokenSerializer, RoleSerializer

# from jwt authorization and utils files 
from leave_management.jwt_authorization import JWTAuthorization

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"User registered successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.data.get("username") 
        password = serializer.data.get("password") 
       
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"message":"Invalid credentials", "status":"error"}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)  # Login user 
        
        token = get_tokens_for_user(user) # Generate token 

        token, is_created = Token.objects.get_or_create(access_token=token.get("access"), refresh_token=token.get("refresh"), user=user)
        
        return Response({"message":"User logged in successfully..!!", "user_data": serializer.data, "token":TokenSerializer(token).data, "status":"success"}, status=status.HTTP_200_OK)


class RoleView(APIView):

    permission_classes = [JWTAuthorization]

    def post(self, request):

        if not request.user.role.name == "admin" and  not request.user.role.name == "HR" :
            return Response({"message":"You are not authorized to perform this action only human resource or admin created the roles", "status":"error"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Role created successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
       
    def put(self, request, id):

        role = Role.objects.filter(id=id, status=True)
        if not role:
            return Response({"message":"Role not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.role.name == "admin" and  not request.user.role.name == "HR" :
            return Response({"message":"You are not authorized to perform this action only human resource or admin updated the roles", "status":"error"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = RoleSerializer(instance=role.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Role updated successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_200_OK)
                         
    def delete(self, request, id):
        role = Role.objects.filter(id=id, status=True)
        if not role:
            return Response({"message":"Role not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.role.name == "admin" and  not request.user.role.name == "HR" :
            return Response({"message":"You are not authorized to perform this action only human resource or admin delete the roles", "status":"error"}, status=status.HTTP_401_UNAUTHORIZED)
        
        role.delete()
        return Response({"message":"Role deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)





