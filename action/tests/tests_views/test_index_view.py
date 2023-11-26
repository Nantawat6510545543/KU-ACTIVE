from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user
from action.tests.end_to_end_base import EndToEndTestBase

from selenium.webdriver.support.ui import Select


class ActivityIndexViewTests(TestCase):
    """Test cases for the activity index view."""

    def setUp(self) -> None:
        """Set up test user."""
        self.user = create_user()

    def test_no_activity_available(self):
        """
        Test that there are no activities on the index page if none have been created.

        1. Attempt to access the index page.
        2. Assert that the response status code is 200.
        3. Assert that the 'activity_list' in the context is an empty list.
        """
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'], [])

    def test_view_available_activity(self):
        """
        Test that an activity is shown on the index page if it is available.

        1. Create a new activity.
        2. Attempt to access the index page.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity_list' in the context contains the newly created activity.
        """
        new_activity = create_activity(self.user)
        response = self.client.get(reverse('action:index'))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['activity_list'],
                              [new_activity])

    def test_not_published_activity(self):
        """
        Test that a new activity that has not been published is not shown on the index page.

        1. Create a new activity with a future publication date.
        2. Attempt to access the index page.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity_list' in the context is an empty list.
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
        Test that only published activities are shown on the index page.

        1. Create a new activity with a future publication date.
        2. Create an old activity.
        3. Attempt to access the index page.
        4. Assert that the response status code is 200.
        5. Assert that the 'activity_list' in the context contains only the old activity.
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
        Test that all published activities are shown on the index page.

        1. Create multiple activities with different titles.
        2. Attempt to access the index page.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity_list' in the context contains all activities in descending order based on their titles.
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
        Test that all published activities from any user are shown on the index page.

        1. Create activities from different users.
        2. Attempt to access the index page.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity_list' in the context contains all activities in descending order based on their titles.
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
        Test that guests are redirected when attempting to view pages with tags.

        1. Attempt to access the index page with the tags 'registered', 'favorited' and 'friend_joined'.
        2. Assert that all response status code is 302 (redirected).
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
        Test that authenticated users can view pages with tags.

        1. Log in the user.
        2. Attempt to access the index page with the tags 'registered', 'favorited' and 'friend_joined'.
        3. Assert that all response status code is 200.
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
    """End-to-end tests for the activity index view."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Define a username and password.
        2. Create a user with the defined username and password.
        3. Define the view name.
        """
        self.name = 'user1'
        self.password = 'pass1'
        self.user = create_user(self.name, self.password)
        self.view = 'action:index'

    def test_search_activity_by_title(self):
        """
        Test searching for an activity by title.

        1. Create an activity.
        2. Navigate to the index page.
        3. Select "Title" as the search criteria.
        4. Input the activity title into the search bar.
        5. Click the submit button.
        6. Find the activity element and assert that the title is present in its text.
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
        Test searching for an activity by owner name.

        1. Create an activity.
        2. Navigate to the index page.
        3. Select "Owner" as the search criteria.
        4. Input the owner's name into the search bar.
        5. Click the submit button.
        6. Find the activity element and assert that the owner's name is present in its text.
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
