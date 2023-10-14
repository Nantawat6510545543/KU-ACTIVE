from django.test import TestCase
from action.models import User


class UserModelTest(TestCase):
    """
    Test case for the User model.

    This class contains test methods to verify
    the attributes and behavior of the User model.
    """
    def test_username_attribute(self):
        """
        Test the username attribute of the User model.
        """
        user = User(username="testuser")
        user.save()
        self.assertEqual(user.username, "testuser")

    def test_password_attribute(self):
        """
        Test the password attribute (set and check) for the User model.
        """
        user = User(username="testuser")
        user.set_password("testpassword")  # Set the user's password
        user.save()
        self.assertTrue(user.check_password("testpassword"))  # Check password

    def test_email_attribute(self):
        """
        Test the email attribute of the User model.
        """
        user = User(email="test@example.com")
        user.save()
        self.assertEqual(user.email, "test@example.com")

    def test_first_name_attribute(self):
        """
        Test the first_name attribute of the User model.
        """
        user = User(first_name="John")
        user.save()
        self.assertEqual(user.first_name, "John")

    def test_last_name_attribute(self):
        """
        Test the last_name attribute of the User model.
        """
        user = User(last_name="Doe")
        user.save()
        self.assertEqual(user.last_name, "Doe")

    def test_is_staff_attribute(self):
        """
        Test the is_staff attribute of the User model.
        """
        user = User(is_staff=True)
        user.save()
        self.assertTrue(user.is_staff)

    def test_is_active_attribute(self):
        """
        Test the is_active attribute of the User model.
        """
        user = User(is_active=True)
        user.save()
        self.assertTrue(user.is_active)
