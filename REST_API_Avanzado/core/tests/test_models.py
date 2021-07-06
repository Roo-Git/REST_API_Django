from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@datadosis.com', password='testpass'):
    """ Crear usuario de Ejemplo """
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):

  def test_create_user_with_email_succesfuly(self):
    """ Probar crear un nuevo usuario con un email correctamente """
    email = 'test@datadosis.com'
    password = 'Testpass123'
    user = get_user_model().objects.create_user(
      email=email,
      password=password,
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))

  def test_new_user_email_normalized(self):
    """ Testea email para nuevo usuiario normalizado """
    email = 'test@DATADOSIS.COM'
    user = get_user_model().objects.create_user(email,'Testpass123')

    self.assertEqual(user.email, email.lower())

  def test_new_user_invalid_email(self):
    """ Nuevo Usuario Email Invalido """
    with self.assertRaises(ValueError):
        get_user_model().objects.create_user(None,'Testpass123')
  
  def test_create_new_superuser(self):
    """ Probar Super Usuario Creado """
    email = 'test@datadosis.com'
    password = 'Testpass123'
    user = get_user_model().objects.create_superuser(
      email=email,
      password=password,
    )

    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)
  
  def test_tag_str(self):
    """ Probar representación en cadena de texto del tag """
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='Meat'
    )

    self.assertEqual(str(tag), tag.name)

  def test_ingredient_str(self):
    """ Probar representación en cadena de texto del ingrediente """
    ingredient = models.Ingredient.objects.create(
      user=sample_user(),
      name='Banana'
    )

    self.assertEqual(str(ingredient), ingredient.name)