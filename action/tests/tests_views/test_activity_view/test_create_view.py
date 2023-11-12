from datetime import timedelta

from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user
from django.utils import timezone


class ActivityCreateViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)

    def test_access_activity_create_guest(self):
        """
        Unauthenticated users are not allowed to access this function.
        Should be redirected to the index page.
        """
        response = self.client.get(reverse('action:create'))
        self.assertEqual(response.status_code, 302)

    def test_access_activity_create_authenticated(self):
        """
        Authenticated users are allowed to use this function.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))
        self.assertEqual(response.status_code, 200)

    def test_initial_values(self):
        """
        Initial value should be added.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))
        form = response.context['form']

        self.assertEqual(form.initial['owner'], self.user)
        self.assertEqual(form.initial['pub_date'].date(), timezone.now().date())
        self.assertEqual(form.initial['end_date'].date(), (timezone.now() + timedelta(days=1)).date())
        self.assertEqual(form.initial['start_date'].date(), (timezone.now() + timedelta(days=2)).date())
        self.assertEqual(form.initial['last_date'].date(), (timezone.now() + timedelta(days=3)).date())
