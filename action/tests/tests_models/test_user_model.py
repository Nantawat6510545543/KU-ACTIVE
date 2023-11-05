from django.test import TestCase
from action.tests import utils


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'active': True,
        }
        self.user = utils.create_user(**self.user_data)

    def test_user_attributes(self):
        user = self.user  # shorter reference
        data = self.user_data

        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
