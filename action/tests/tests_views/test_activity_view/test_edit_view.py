from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user


class ActivityEditViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)
        self.activity = create_activity(self.user)

    def test_access_activity_edit_guest(self):
        """
        Unauthenticated users are not allowed to access this function.
        Should be redirected to the index page.
        """
        url = reverse('action:edit', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_access_activity_edit_authenticated(self):
        """
        Authenticated users are allowed to edit their own activity.
        """
        self.client.force_login(self.user)
        url = reverse('action:edit', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # TODO: BUGS HERE
    # def test_others_edit_activity(self):
    #     """
    #     Nobody is allowed to edit others activities.
    #     """
    #     user_data = {"email": "test2@example.com"}
    #     another_user = create_user(username="Jane", password="abc", **user_data)
    #     self.client.force_login(another_user)
    #     url = reverse('action:edit', args=(self.activity.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
