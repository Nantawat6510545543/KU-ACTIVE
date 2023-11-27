from datetime import timedelta, datetime

from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user, USER_DATA_1
from django.utils import timezone
from action.views.activity.activity_create_view import ActivityCreateView


class ActivityCreateViewTests(TestCase):
    """Test cases for the ActivityCreateView."""

    def setUp(self) -> None:
        """Set up the test environment by creating a test user."""
        self.user = create_user(**USER_DATA_1)

    def test_access_activity_create_guest(self):
        """
        Test whether unauthenticated users are allowed to access the activity creation view.

        Unauthenticated users should be redirected to the index page.
        """
        response = self.client.get(reverse('action:create'))
        self.assertEqual(response.status_code, 302)

    def test_access_activity_create_authenticated(self):
        """
        Test whether authenticated users are allowed to access the activity creation view.

        Authenticated users should be able to access the view with a status code of 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))
        self.assertEqual(response.status_code, 200)

    def test_initial_values(self):
        """
        Test the initial values set in the activity creation form.

        Initial values should be set correctly for the activity creation form.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:create'))
        form = response.context['form']

        self.assertEqual(form.initial['owner'], self.user)
        self.assertEqual(form.initial['pub_date'].date(), timezone.now().date())
        self.assertEqual(form.initial['end_date'].date(),
                         (timezone.now() + timedelta(days=1)).date())
        self.assertEqual(form.initial['start_date'].date(),
                         (timezone.now() + timedelta(days=2)).date())
        self.assertEqual(form.initial['last_date'].date(),
                         (timezone.now() + timedelta(days=3)).date())

    def test_form_valid_create(self):
        """
        Test the behavior when a valid form is submitted for creating an activity.

        The form should be submitted successfully, and a success message should be displayed.
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
        # A successful message should be shown.
        self.assertContains(response, 'Activity created successfully.')

    def test_form_invalid_create(self):
        """
        Test the behavior when an invalid form is submitted for creating an activity.

        The form submission should fail, and an error message should be displayed.
        """
        now = datetime.now()
        # invalid data, pub_date should be today.
        form_data = {
            'pub_date': now - timedelta(days=2),
            'end_date': now + timedelta(days=1),
            'start_date': now + timedelta(days=2),
            'last_date': now + timedelta(days=3),
        }
        self.client.force_login(self.user)

        response = self.client.post(reverse('action:create'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        # A fail message should be shown.
        self.assertTrue(response.context['form'].errors)

    def test_get_success_url(self):
        """
        Test the success URL after successfully creating an activity.

        The success URL should be the index page for activities.
        """
        view = ActivityCreateView()
        success_url = view.get_success_url()
        # A successful action should be redirected to the index page.
        self.assertEqual(success_url, reverse('action:index'))
