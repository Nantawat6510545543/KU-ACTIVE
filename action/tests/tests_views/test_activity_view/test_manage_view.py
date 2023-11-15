from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user


class ActivityManageViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)
        self.activity = create_activity(self.user)

    def test_manage_activity_guest(self):
        """
        Guest should not have a permission to access this page.
        Should be redirected.
        """
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manage_activity_authenticated(self):
        """
        Authenticated users should have a permission to access this page.
        """
        self.client.force_login(self.user)
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_guest_delete_activity(self):
        """
        Guest should not have permission to access this feature.
        Should be redirected.
        """
        url = reverse('action:delete_activity', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # TODO: Redirect can't use with this feature
    # def test_delete_others_activity(self):
    #     """
    #     Any authenticated user should not be able to delete others activities.
    #     Should be redirected.
    #     """
    #     user_data = {"email": "test2@example.com"}
    #     other = create_user(username="Tim", password="abc", **user_data)
    #     self.client.force_login(other)
    #     url = reverse('action:delete_activity', args=(self.activity.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_delete_self_activity(self):
    #     """
    #     Authenticated users can delete their own activity.
    #     """
    #     self.client.force_login(self.user)
    #     url = reverse('action:delete_activity', args=(self.activity.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
    #     # TODO: Check message instead
    #     self.assertIs(response.context['messages'], "a")
