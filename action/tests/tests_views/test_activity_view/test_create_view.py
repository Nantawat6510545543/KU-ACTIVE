from datetime import timedelta

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from mysite import settings
from action.models import *
from action.tests import utils
from action.tests.utils import *
from action.forms.activity_form import *


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

    # TODO: FIX BELOW
    def test_valid_activity_creation(self):
        """
        Newly created activity should be added to the database.
        If the activity is valid.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))

    # def test_invalid_activity_creation(self):
    #     """
    #     Test that new activity should not be able to create.
    #     If the activity is invalid.
    #     """
    #     self.client.force_login(self.user)
    #     initial_count = Activity.objects.count()
    #
    #     response = self.client.post(reverse('action:create'), {})
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Activity.objects.count(), initial_count)
