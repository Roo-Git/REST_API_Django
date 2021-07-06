from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """ Probar los API tags disponibles publicamente """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Prueba que Login sea requerido para obtener los tags """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """ Probar los API tags disponibles privados """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
          'test@datadosis.com',
          'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        """ Probar obtener tags """
        Tag.objects.create(user=self.user, name='Meat')
        Tag.objects.create(user=self.user, name='Banana')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
      
    def test_tags_limited_to_user(self):
        """ Probar que los tags retornados sean del usuario """
        user2 = get_user_model().objects.create_user(
          'user2@datadosis.com',
          'testpass'
        )
        Tag.objects.create(user=user2, name='Raspberry')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
