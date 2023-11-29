from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.messages import get_messages

from action.models import ActivityStatus
from action.tests.end_to_end_base import EndToEndTestBase
from action.tests.utils import create_user, create_activity, USER_DATA_1


class ActivityDetailViewTests(TestCase):
    """Test case for the views related to activity details."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create a user.
        2. Create an activity with the user.
        """
        self.user = create_user(**USER_DATA_1)
        self.activity = create_activity(self.user)

    def test_view_activity_detail_guest(self):
        """
        Test the activity detail view for a guest user.

        1. Attempt to view the detail of an existing activity.
        2. Assert that the response status code is 200.
        3. Assert that the 'activity' key is present in the context.
        4. Assert that the 'activity' in the context matches the created activity.
        """
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_activity_detail_upcoming(self):
        """
        Test the activity detail view for an upcoming activity.

        1. Create an upcoming activity.
        2. Attempt to view the detail of the upcoming activity.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity' key is present in the context.
        5. Assert that the 'activity' in the context matches the created upcoming activity.
        """
        future_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        future_activity = create_activity(self.user, **future_date)
        url = reverse('action:detail', args=(future_activity.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], future_activity)

    def test_view_activity_detail_authenticated(self):
        """
        Test the activity detail view for an authenticated user.

        1. Log in the user.
        2. Attempt to view the detail of an existing activity.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity' key is present in the context.
        5. Assert that the 'activity' in the context matches the created activity.
        """
        self.client.force_login(self.user)
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_nonexistent_activity_detail(self):
        """
        Test attempting to view details of a nonexistent activity.

        1. Attempt to view the detail of a nonexistent activity.
        2. Assert that the response status code is 302 (redirect).
        3. Assert that the response redirects to the index page.
        4. Assert that a message indicating that the activity does not exist is present.
        """
        nonexistent_act_id = 999
        url = reverse('action:detail', args=(nonexistent_act_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('action:index'))
        # Check the messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Activity does not exist.')


class ActivityDetailViewTestsE2E(EndToEndTestBase):
    """End-to-end test case for the activity detail view."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Call the parent class's setup method.
        2. Create a user.
        3. Set the view attribute.
        """
        super().setUp()
        self.name = 'user1'
        self.password = 'pass1'
        self.user = create_user(self.name, self.password)
        self.view = 'action:detail'

    def participated_count(self):
        """Get the count of activities the user has participated in."""
        return ActivityStatus.objects.filter(
            id__in=self.user.participated_activity).count()

    def favorited_count(self):
        """Get the count of activities the user has favorited."""
        return ActivityStatus.objects.filter(
            id__in=self.user.favorited_activity).count()

    def perform_action(self, action_button, expected_initial_text,
                       expected_final_text, count_function):
        """
        Perform a user action (participate or favorite) and check the result.

        Parameters:
            - `action_button`: The class name of the action button.
            - `expected_initial_text`: The expected text on the button before performing the action.
            - `expected_final_text`: The expected text on the button after performing the action.
            - `count_function`: The function to get the count of user activities.

        Steps:
            1. Create an activity.
            2. Open the activity detail view.
            3. Check if the user count is initially 0.
            4. Click on the button and check initial text.
            5. Check if the button text changes after performing the action.
            6. Check if the user count is now 1.
            7. Undo the action and check button text.
            8. Check if the user count is back to 0.
        """
        # Create activity
        activity = create_activity(self.user)
        self.open(self.view, activity.id)

        # Ensure user count is initially 0
        self.assertEqual(count_function(), 0)

        # Click on the button and check initial text
        button = self.find_by_class(action_button)
        self.assertEqual(button.text, expected_initial_text)
        button.click()

        # Check if button text changes after performing the action
        button = self.find_by_class(action_button)
        self.assertEqual(button.text, expected_final_text)

        # Check if user count is now 1
        self.assertEqual(count_function(), 1)

        # Undo the action and check button text
        button.click()
        button = self.find_by_class(action_button)
        self.assertEqual(button.text, expected_initial_text)

        # Ensure user count is back to 0
        self.assertEqual(count_function(), 0)

    def test_view_activity_without_login(self):
        """
        Test viewing activity details without login.

        1. Create an activity.
        2. Open the activity detail view.
        3. Find the 'activity-details' element.
        4. Check the presence of specific classes within the element.
        """
        activity = create_activity(self.user)
        self.open(self.view, activity.id)

        # Find the 'activity-details'
        details = self.find_by_class("activity-details")

        # List of classes to check
        classes_to_check = ["Description", "full-detail",
                            "activity-general-information"]

        # Iterate over the classes and check their presence
        for class_name in classes_to_check:
            element = self.find_by_class(class_name, details)
            self.assertTrue(element, f"{class_name} class not found")

    def test_participate_and_favorited(self):
        """
        Test participating in and favoriting an activity.

        1. Log in the user.
        2. Test participating:
            - Perform the participation action.
            - Check the user count and undo the action.
        3. Test favoriting:
            - Perform the favoriting action.
            - Check the user count and undo the action.
        """
        self.login(self.name, self.password)

        # Test Participate
        self.perform_action("Participate-btn", 'Participate', 'Leave',
                            self.participated_count)

        # Test Favorited
        self.perform_action("Favorite-btn", 'Favorite', 'Un-favorite',
                            self.favorited_count)

    def test_unable_to_participate_upcoming_activity(self):
        """
        Test unable to participate in an upcoming activity.

        1. Log in the user.
        2. Create an upcoming activity.
        3. Open the activity detail view.
        4. Attempt to participate.
        5. Check if an alert message indicates that registration has not yet opened.
        """
        self.login(self.name, self.password)

        future_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        future_activity = create_activity(self.user, **future_date)
        self.open(self.view, future_activity.id)

        participate_button = self.find_by_class("Participate-btn")
        participate_button.click()

        # Check the messages.
        messages = self.find_by_class("alert-msg")
        except_text = 'Registration for the activity has not yet opened.'
        self.assertIn(except_text, messages.text)
