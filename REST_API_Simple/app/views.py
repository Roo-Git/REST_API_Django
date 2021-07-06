from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from app import serializers, models, permissions

# Create your views here.

class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
        'Usamos métodos HTTP como funciones (get, post, patch, put, delete)',
        'Es similar a una vista tradicional de Django',
        'Nos da el mayor control sobre la lógica de nuestra applicación',
        'Esta mapeado manualmente a los URLs',
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Actualizar un objeto """
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """ Actualización parcial de un objeto """
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """ Borrar un objeto """
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
  """ Test API ViewSet """
  serializer_class = serializers.HelloSerializer
  
  def list(self, request):
    """ Retornar Mensaje de Hola Mundo """
    
    a_viewset= [
      'Usa acciones (list, create, retrieve, update, partial_update',
      'Automaticamente mapea a los URLs usando Routers',
      'Provee más funcionalidad con menos código',
    ]

    return Response({'message': 'Hola', 'a_viewset': a_viewset})
  
  def create(self, request):
    """ Crear nuevo mensaje de hola mundo """
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        message = f"Hola {name}"
        return Response({'message': message})
    else:
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
  def retrieve(self, request, pk=None):
      """ Obtiene un Objeto y su ID """   
      return Response({'http_method': 'GET'})

  def update(self, request, pk=None):
      """ Actualiza un objeto """
      return Response({'http_method': 'PUT'})
  
  def partial_update(self, request, pk=None):
      """ Actualiza parcialmente objeto """
      return Response({'http_method': 'PATCH'})

  def destroy(self, request, pk=None):
      """ Borra un objeto """
      return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Crear y Actualizar Perfiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """ Crea Tokens de Auth de Usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Maneja el Crear, Leer y Actualizar el Profile Feed """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """ Setear el Perfil de Usuario para el Usuario que esta Logeado """
        serializer.save(user_profile=self.request.user)

