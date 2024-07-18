# from django 
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.db.models import Q

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# from models and serializer
from .models import Token, Role
from user_registration.serializer import UserRegistrationSerializer, LoginSerializer, TokenSerializer, RoleSerializer

# from jwt authorization and utils files 
from leave_management.jwt_authorization import JWTAuthorization, CheckPermission
from leave_management.utils import handle_exceptions
from leave_management.renderers import UserRenderer
from datetime import datetime
from django.apps import apps

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"User registered successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
    
    @handle_exceptions()
    def get(self, request):
        role_data = Role.objects.all().exclude(Q(name="HR") | Q(name="admin"))
        return render(request, "user/register.html", {"data":role_data})
    

class LoginView(APIView):

    renderer_classes = [UserRenderer]

    @handle_exceptions()
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
        request.session["access_token"] = token.get("access")
        request.session["refresh_token"] = token.get("refresh")
        token, is_created = Token.objects.get_or_create(access_token=token.get("access"), refresh_token=token.get("refresh"), user=user)
        # result = Response({"message":"User logged in successfully..!!", "user_data": serializer.data, "token":TokenSerializer(token_obj).data, "status":"success"}, status=status.HTTP_200_OK)
        # result.set_cookie("access", token.get("access"))
        # result.set_cookie("refresh", token.get("refresh"))
        # return result
        
        return Response({"message":"User logged in successfully..!!", "user_data": serializer.data, "token":TokenSerializer(token).data, "status":"success"}, status=status.HTTP_200_OK)
    
    @handle_exceptions()
    def get(self, request):
        return render(request, "user/login.html")



class RoleView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Role created successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)

    @handle_exceptions()   
    def put(self, request, id):

        role = Role.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not role:
            return Response({"message":"Role not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RoleSerializer(instance=role.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Role updated successfully..!!", "data":serializer.data, "status":"success"}, status=status.HTTP_200_OK)

    @handle_exceptions()                  
    def delete(self, request, id):
        role = Role.objects.filter(id=id, status=True, deleted_at__isnull=True)
        if not role:
            return Response({"message":"Role not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        role.update(deleted_at=datetime.now(), deleted_by=request.user.id)
        return Response({"message":"Role deleted successfully..!!", "status":"success"}, status=status.HTTP_200_OK)


class UpdateRoleStatus(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [JWTAuthorization, CheckPermission]
    
    @handle_exceptions()
    def put(self, request, id):

        role = Role.objects.filter(id=id, deleted_at__isnull=True)
        if not role:
            return Response({"message":"Role not found", "status":"error"}, status=status.HTTP_404_NOT_FOUND)
        
        if role.first().status:
            role.update(status=False)
        else:
            role.update(status=True)
        
        return Response({"message":"Status updated successfully..!!", "status":"success"}, status=status.HTTP_200_OK)
        





