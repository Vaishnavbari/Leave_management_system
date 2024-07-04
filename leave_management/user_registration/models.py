from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from leave_management.settings import AUTH_USER_MODEL

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted_by = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="RoleDeletedBy")  

    def __str__(self) -> str:
        return self.name

class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password, role=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        
        if not email:
            raise ValueError("Users must have an email address")
        
        if not username:
            raise ValueError("Users must have username")
        
        if not password:
            raise ValueError("Users must have password")
        
        if not role:
            raise ValueError("User must have role")
    
        # role_instance, is_created = Role.objects.get_or_create(name="admin")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, role=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        role_instance, is_created = Role.objects.get_or_create(name="admin")

        user = self.create(
            email=email,
            username=username,
            role=role_instance
        )

        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MyUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    

class Token(models.Model):
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)