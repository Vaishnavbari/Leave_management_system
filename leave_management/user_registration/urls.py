from django.urls import path
from . import views

urlpatterns = [
 # User  
 path("register", views.UserView.as_view(), name="Register"),
 path("login", views.LoginView.as_view(), name="Login"),

# Role
 path("add/role", views.RoleView.as_view(), name="AddRole"),
 path("update/role/<int:id>", views.RoleView.as_view(), name="UpdateRole"),
 path("delete/role/<int:id>", views.RoleView.as_view(), name="DeleteRole"),

#  Update status 
 path("update/role-status/<int:id>", views.UpdateRoleStatus.as_view(), name="UpdateRoleStatus"),
]
