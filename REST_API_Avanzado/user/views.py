from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework import generics, authentication, permissions


class CreateUserView(generics.CreateAPIView):
    """ Crear nuevo usuario en el sistema """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ Crear nuevo auth token para usuario """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manejar el usuario autenticado """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
      """ Obtener y Retornar Usuario Autenticado """
      return self.request.user