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

        # Check every attribute of model object equal to a manual object
        for key, value in self.user_data.items():
            if key == 'password':  # can't compare password directly because it's hashed
                self.assertTrue(user.check_password(value))
            else:
                self.assertEqual(getattr(user, key), value)
