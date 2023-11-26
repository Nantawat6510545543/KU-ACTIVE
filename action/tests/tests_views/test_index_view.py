from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user
from action.tests.end_to_end_base import EndToEndTestBase

from selenium.webdriver.support.ui import Select


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
        create_activity(self.user, **update_date)  # new activity
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
        activity_1 = create_activity(self.user, title="Football")
        activity_2 = create_activity(self.user, title="Run")
        activity_3 = create_activity(self.user, title="Walk")

        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [activity_3, activity_2, activity_1])

    def test_multiple_available_activity_and_owner(self):
        """
        All published activity from any user should be shown.
        """
        activity_1 = create_activity(self.user, title="Football")

        jane = create_user(username="Jane")
        activity_2 = create_activity(jane, title="Run")

        john = create_user(username="John")
        activity_3 = create_activity(john, title="Walk")

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
    def setUp(self):
        self.name = 'user1'
        self.password = 'pass1'
        self.user = create_user(self.name, self.password)
        self.view = 'action:index'

    def test_search_activity_by_title(self):
        """
        Search by title should show correctly.
        """
        activity_1_data = {"title": "activity 1"}
        create_activity(self.user, **activity_1_data)

        # Navigate to the index page
        url = self.getUrl(self.view)
        self.browser.get(url)

        # Select "Title" as the search criteria
        search_criteria_dropdown_class_name = "search-criteria"
        search_criteria_dropdown = Select(self.find_by_class(search_criteria_dropdown_class_name))
        search_criteria_dropdown.select_by_visible_text("Title")

        # Find the search bar element by class name
        search_bar_class_name = "search-bar"
        search_bar = self.find_by_class(search_bar_class_name)
        # Input the activity name into the search bar
        search_bar.send_keys(activity_1_data["title"])

        # Find the submit button element by class name
        submit_button_class_name = "search-button"
        submit_button = self.find_by_class(submit_button_class_name)
        # Click the submit button
        submit_button.click()

        activity_element = self.find_by_class("activity")
        self.assertIn(activity_1_data["title"], activity_element.text)

    def test_search_activity_by_owner(self):
        """
        Search by Owner name should show correctly.
        """
        # Create an activity
        activity_1_data = {"title": "activity 1"}
        create_activity(self.user, **activity_1_data)

        # Navigate to the index page
        url = self.getUrl(self.view)
        self.browser.get(url)

        # Select "Owner" as the search criteria
        search_criteria_dropdown_class_name = "search-criteria"
        search_criteria_dropdown = Select(self.find_by_class(search_criteria_dropdown_class_name))
        search_criteria_dropdown.select_by_visible_text("Owner")

        # Find the search bar element by class name
        search_bar_class_name = "search-bar"
        search_bar = self.find_by_class(search_bar_class_name)
        # Input the owner's name into the search bar
        search_bar.send_keys(self.user.username)

        # Find the submit button element by class name
        submit_button_class_name = "search-button"
        submit_button = self.find_by_class(submit_button_class_name)
        # Click the submit button
        submit_button.click()

        activity_element = self.find_by_class("activity")
        self.assertIn(self.user.username, activity_element.text)
