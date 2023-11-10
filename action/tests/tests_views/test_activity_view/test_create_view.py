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

# TODO: THERE ARE STILL ERROR IN THESE CODE, PLEASE WAIT!!!!!!!
class ActivityCreateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    # TODO: THERE ARE STILL ERROR IN THESE CODE, PLEASE WAIT!!!!!!!
    def test_activity_create_redirect(self):
        self.client.force_login(self.user)
        data = {
            "title": "Test",
            "pub_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1),
            "start_date": timezone.now() + timezone.timedelta(days=2),
            "last_date": timezone.now() + timezone.timedelta(days=3),
            "description": "Description",
            "place": "Location",
            "full_description": "FullDescription",
            "participant_limit": None,
            "tags": ['Tag1'],
        }
        response = self.client.post(reverse('action:create'), data)
        self.assertRedirects(response, reverse('action:index'))

    # TODO: THERE ARE STILL ERROR IN THESE CODE, PLEASE WAIT!!!!!!!
    def test_activity_creation(self):
        self.client.force_login(self.user)
        initial_count = Activity.objects.count()
        data = {
            "title": "Test",
            "pub_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1),
            "start_date": timezone.now() + timezone.timedelta(days=2),
            "last_date": timezone.now() + timezone.timedelta(days=3),
            "description": "Description",
            "place": "Location",
            "full_description": "FullDescription",
            "participant_limit": None,
            "tags": ['Tag1'],
        }

        response = self.client.post(reverse('action:create'), data)

        self.assertEqual(response.status_code, 302)  # Check if the form submission was successful
        self.assertEqual(Activity.objects.count(), initial_count + 1)  # Check if a new activity was created

    # TODO: THERE ARE STILL ERROR IN THESE CODE, PLEASE WAIT!!!!!!!
    def test_initial_values(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))
        form = response.context['form']

        self.assertEqual(form.initial['owner'], self.user)
        self.assertEqual(form.initial['pub_date'].date(), timezone.now().date())
        self.assertEqual(form.initial['end_date'].date(), (timezone.now() + timedelta(days=1)).date())
        self.assertEqual(form.initial['start_date'].date(), (timezone.now() + timedelta(days=2)).date())
        self.assertEqual(form.initial['last_date'].date(), (timezone.now() + timedelta(days=3)).date())

    # TODO: THERE ARE STILL ERROR IN THESE CODE, PLEASE WAIT!!!!!!!
    def test_invalid_form_submission(self):
        self.client.force_login(self.user)
        initial_count = Activity.objects.count()

        # Submit an invalid form by omitting required fields
        response = self.client.post(reverse('action:create'), {})

        self.assertEqual(response.status_code, 200)  # Check if the form is re-rendered on failure
        self.assertEqual(Activity.objects.count(), initial_count)  # Check that no new activity was created
