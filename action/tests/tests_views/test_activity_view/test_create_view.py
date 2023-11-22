from datetime import timedelta, datetime

from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user
from django.utils import timezone
from action.views.activity.create_view import ActivityCreateView


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

    def test_form_valid_create(self):
        """
        Test sending valid form, Should show success message.
        """
        now = datetime.now()
        # Correct data.
        form_data = {
            'owner': self.user.pk,
            'title': 'Test Title',
            'pub_date': now,
            'end_date': now + timedelta(days=1),
            'start_date': now + timedelta(days=2),
            'last_date': now + timedelta(days=3),
            'description': 'Test Description',
            'place': 'Test Place',
            'full_description': 'Test Full Description',
        }
        self.client.force_login(self.user)

        response = self.client.post(reverse('action:create'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        # A successful message should have been shown.
        self.assertContains(response, 'Activity created successfully.')

    def test_form_invalid_create(self):
        """
        Test sending invalid form, Should show fail message.
        """
        now = datetime.now()
        # invalid data, pub_date should be today.
        form_data = {
            'pub_date': now - timedelta(days=1),
            'end_date': now + timedelta(days=1),
            'start_date': now + timedelta(days=2),
            'last_date': now + timedelta(days=3),
        }
        self.client.force_login(self.user)

        response = self.client.post(reverse('action:create'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        # A fail message should have been shown.
        self.assertTrue(response.context['form'].errors)

    def test_get_success_url(self):
        """
        Successfully create should redirect user to index page.
        """
        view = ActivityCreateView()
        success_url = view.get_success_url()
        # A successful action should be redirected to the index page.
        self.assertEqual(success_url, reverse('action:index'))