from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """ Permite al Usuario Editar su Propio Perfil """

    def has_object_permission(self, request, view, obj):
        """ Chequear si el Usuario esta Intentando Editar su Propio Perfil """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id 

class UpdateOwnStatus(permissions.BasePermission):
    """ Permite al Usuario Actualizar su Propio Status Feed """

    def has_object_permission(self, request, view, obj):
        """ Chequear si el Usuario esta Intentando Editar su Propio Perfil """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile_id == request.user.id 
