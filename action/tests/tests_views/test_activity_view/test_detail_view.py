import time

# from django.urls import reverse
from django.test import TestCase
# from django.utils import timezone

# from action.tests.utils import create_activity, create_user, create_request
from action.tests.utils import *
from action.tests.end_to_end_base import EndToEndTestBase


class ActivityDetailViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)
        self.activity = create_activity(self.user)

    def test_access_activity_detail_guest(self):
        """
        Anyone should be able to view the detail of any available activity.
        """
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_activity_detail_authenticated(self):
        """
        Authenticated users should be able to view
        the detail of any available activity.
        """
        self.client.force_login(self.user)
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unavailable_activity_detail_redirect(self):
        """
        Should not be able to view the detail of unavailable activity.
        Should be redirected to index instead.
        """
        update_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        new_activity = create_activity(self.user, **update_date)
        url = reverse('action:detail', args=(new_activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)


class ActivityDetailViewTestsE2E(EndToEndTestBase):
    def setUp(self):
        super().setUp()

        self.user = create_user(username='user1', password='pass1')
        self.login(username='user1', password='pass1')
        self.activity = create_activity(self.user)
        self.view = 'action:detail'

        self.url = self.getUrl(self.view, (self.activity.id,))
        self.browser.get(self.url)

    def participated_count(self):
        return ActivityStatus.objects.filter(
            id__in=self.user.participated_activity).count()

    def find_participate_button(self):
        return self.browser.find_element(self.by.CLASS_NAME, "Participate")

    def test_participate(self):
        # Ensure user is not participating initially
        self.assertEqual(self.participated_count(), 0)

        # Participate and check button text
        participate_button = self.find_participate_button()
        self.assertEqual(participate_button.text, 'Participate')
        participate_button.click()

        # Check if button text changes after participating
        participate_button = self.find_participate_button()
        self.assertEqual(participate_button.text, 'Leave')

        # Check if user is now participating
        self.assertEqual(self.participated_count(), 1)

        # Leave and check button text
        participate_button.click()
        participate_button = self.find_participate_button()
        self.assertEqual(participate_button.text, 'Participate')

        # Ensure user is no longer participating
        self.assertEqual(self.participated_count(), 0)
