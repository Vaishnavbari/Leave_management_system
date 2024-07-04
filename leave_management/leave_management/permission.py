from rest_framework.response import Response
from rest_framework import status


#  check user permission
def check_permission(user):
     
     if not user.role.name == "admin" and  not user.role.name == "HR" :
        return False
      
     return True


