from rest_framework import serializers

from app import models

class HelloSerializer(serializers.Serializer):
  """ Serializa un campo para probar nuestra APIView """
  name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
  """ Serializa Objeto de Perfil de Usuario """

  class Meta:
    model = models.UserProfile
    fields = ('id', 'email', 'name', 'password')
    extra_kwargs = {
        'password': {
          'write_only': True,
          'style': {'input_type': 'password'}
        }
    }
  
  def create(self, validated_data):
      """ Crear y Retornar un Nuevo Usuario """
      user = models.UserProfile.objects.create_user(
          email=validated_data['email'],
          name=validated_data['name'],
          password=validated_data['password']
      )

      return user
  
  def update(self, instance, validated_data):
    """ Handle Updating User Account"""
    if 'password' in validated_data:
        password = validated_data.pop('password')
        instance.set_password(password)
      
        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializador de Profile Feed Items """

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile' : {'read_only':True}}