from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse  

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

import tempfile
import os

from PIL import Image

RECIPES_URL = reverse('recipe:recipe-list')

def image_upload_url(recipe_id):
    """ URL de retorno para imagen subida """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])

def sample_tag(user, name='Main course'):
    """ Crea Tag de ejemplo """
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Cinnamon'):
    """ Crea Ingrediente de ejmplo """
    return Ingredient.objects.create(user=user, name=name)

def detail_url(recipe_id):
    """ Retorna Receta Detail URL """
    return reverse('recipe:recipe-detail', args=[recipe_id])

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
    
    def test_view_recipe_detail(self):
        """ Prueba ver los detalles de una receta """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)


    def test_create_basic_recipe(self):
        """ Test Crear Receta """
        payload = {
            'title': 'Test recipe', 
            'time_minutes': 30, 
            'price': 10.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """ Test crear recetas con Tags """

        tag1= sample_tag(user=self.user, name='Tag 1')
        tag2= sample_tag(user=self.user, name='Tag 2')
        payload = {
            'title': 'Test recipe with two tags', 
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30, 
            'price': 10.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """ Test crear recetas con Ingredientes """

        ingredient1= sample_ingredient(user=self.user, name='Ingredient 1')
        ingredient2= sample_ingredient(user=self.user, name='Ingredient 2')
        payload = {
            'title': 'Test recipe with two ingredients', 
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 30, 
            'price': 15.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

class RecipeImageUploadTests(TestCase):
    """ Test para las subidas de imagenes a la receta """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user', 'testopass')
        self.client.force_authenticate(self.user) 
        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """ Test subir imágenes a receta """  
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """ Test subir una imagen que falla """
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 