from django.test import TestCase
from action.tests import utils


class UserModelTest(TestCase):
    """Test case for the User model."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create a user_data dictionary with user details.
        2. Create a user instance using utils.create_user.
        """
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_active': True,
        }
        self.user = utils.create_user(**self.user_data)

    def test_user_attributes(self):
        """
        Test the attributes of the User model.

        Check if each attribute of the model object is equal to the corresponding value in the data dictionary.
        """
        user = self.user  # shorter reference

        # Check every attribute of model object equal to a manual object
        for key, value in self.user_data.items():
            if key == 'password':  # can't compare password directly because it's hashed
                self.assertTrue(user.check_password(value))
            else:
                self.assertEqual(getattr(user, key), value)
