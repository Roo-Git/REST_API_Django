from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse  

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """ Crear y retornar Receta de ejemplo """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10, 
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

class PublicRecipesApiTestCase(TestCase):
    """ Test de acceso autenticado al API """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@datadosis.com', 
            'testopass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """ Probamos a obtener recetas """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """ Probar que los recetas retornados sean del usuario """
        user2 = get_user_model().objects.create_user(
            'otro@dotadosis.com', 
            'testopass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
    
