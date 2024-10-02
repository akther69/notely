from rest_framework.permissions import BasePermission

# custom permission

class OwnerOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user==obj.owner  #return boolean value