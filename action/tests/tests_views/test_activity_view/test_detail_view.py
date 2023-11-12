from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from action.tests.utils import create_activity, create_user


class ActivityDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.activity = create_activity(self.user)

    def test_activity_detail_redirect(self):
        """
        Anyone should be able to view the detail of any available activity.
        """
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
