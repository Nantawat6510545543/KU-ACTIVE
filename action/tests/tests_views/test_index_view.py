from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user
from action.tests.end_to_end_base import EndToEndTestBase


class ActivityIndexViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_no_activity_available(self):
        """
        There should not be any activity on the index page
        if it has not yet been created.
        """
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'], [])

    def test_view_available_activity(self):
        """
        There should be an activity on the index page
        if that activity was created and is available.
        """
        new_activity = create_activity(self.user)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [new_activity])

    def test_not_published_activity(self):
        """
        The new activity that has not been published yet
        should not be shown.
        """
        update_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        new_activity = create_activity(self.user, **update_date)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'], [])

    def test_activity_published_and_yet(self):
        """
        Only published activity that should be shown.
        """
        update_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        new_activity = create_activity(self.user, **update_date)
        old_activity = create_activity(self.user)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [old_activity])

    def test_multiple_available_activity(self):
        """
        All published activity from a should be shown.
        """
        activity_1_data = {"title": "Football"}
        activity_1 = create_activity(self.user, **activity_1_data)
        activity_2_data = {"title": "Run"}
        activity_2 = create_activity(self.user, **activity_2_data)
        activity_3_data = {"title": "Walk"}
        activity_3 = create_activity(self.user, **activity_3_data)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [activity_3, activity_2, activity_1])

    def test_multiple_available_activity_and_owner(self):
        """
        All published activity from any user should be shown.
        """
        activity_1_data = {"title": "Football"}
        activity_1 = create_activity(self.user, **activity_1_data)
        activity_2_data = {"title": "Run"}
        jane = create_user(username="Jane")
        activity_2 = create_activity(jane, **activity_2_data)
        activity_3_data = {"title": "Walk"}
        john = create_user(username="John")
        activity_3 = create_activity(john, **activity_3_data)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [activity_1, activity_2, activity_3])

    def test_index_with_tag_guest(self):
        """
        Guest should not be able to view pages with tag.
        Should be redirected.
        """
        # Try to access registered page.
        response = self.client.get(reverse('action:index') + "?tag=registered")
        self.assertEqual(response.status_code, 302)
        # Try to access favorited page.
        response = self.client.get(reverse('action:index') + "?tag=favorited")
        self.assertEqual(response.status_code, 302)
        # Try to access friend_joined page.
        response = self.client.get(
            reverse('action:index') + "?tag=friend_joined")
        self.assertEqual(response.status_code, 302)

    def test_index_with_tag_authenticated(self):
        """
        Authenticated users should be able to view pages with tag.
        """
        self.client.force_login(self.user)
        # Try to access registered page.
        response = self.client.get(reverse('action:index') + "?tag=registered")
        self.assertEqual(response.status_code, 200)
        # Try to access favorited page.
        response = self.client.get(reverse('action:index') + "?tag=favorited")
        self.assertEqual(response.status_code, 200)
        # Try to access friend_joined page.
        response = self.client.get(
            reverse('action:index') + "?tag=friend_joined")
        self.assertEqual(response.status_code, 200)


class ActivityIndexViewTestsE2E(EndToEndTestBase):
    pass
