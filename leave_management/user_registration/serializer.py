from rest_framework import serializers
from .models import User, Role
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', "role"]

    def validate(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        password2 = validated_data.get("password2")
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", password):
            raise serializers.ValidationError("Password must contain at least 8 character long, 1 uppercase letter, 1 lowercase letter, and 1 number")
        
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
           
        return super().validate(validated_data)
    
    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        password2 = validated_data.get("password2")
        email = validated_data.get("email")
        role = validated_data.get("role")

        return User.objects.create_user(username=username, password=password, email=email, role=role)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
       model = Role
       fields = ['name']

    def validate(self, validated_data):
        name = validated_data.get("name")
        role = Role.objects.filter(name=name).exists()
        if role:
            raise serializers.ValidationError("Role already exists")
        return super().validate(validated_data)

    def create(self, validated_data):
        return Role.objects.create(name= validated_data.get("name"))
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name") if validated_data.get("name") else instance.name
        instance.save()
        return instance