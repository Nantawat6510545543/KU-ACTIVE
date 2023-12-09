from django.utils import timezone

from action.tests.utils import create_user, create_activity
from action.tests.end_to_end_base import EndToEndTestBase
from action.models import Activity, ActivityStatus


class ActivityTestsE2E(EndToEndTestBase):
    """Test case for the views related to activity creation."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Define a username and password.
        2. Create a user with the defined username and password.
        """
        super().setUp()
        self.name = 'user1'
        self.password = 'pass1'
        self.user = create_user(self.name, self.password)

    def participated_count(self):
        """Get the count of activities the user has participated in."""
        return ActivityStatus.objects.filter(
            activity__in=self.user.participated_activity).count()

    def favorited_count(self):
        """Get the count of activities the user has favorited."""
        return ActivityStatus.objects.filter(
            activity__in=self.user.favorited_activity).count()

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
        self.open('action:detail', activity.id)

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

    def test_view_activity_without_login(self):
        """
        Test viewing activity details without login.

        1. Create an activity.
        2. Open the activity detail view.
        3. Find the 'activity-details' element.
        4. Check the presence of specific classes within the element.
        """
        activity = create_activity(self.user)
        self.open('action:detail', activity.id)

        # Find the 'activity-details'
        details = self.find_by_class("activity-details")

        # List of classes to check
        classes_to_check = ["Description", "full-detail",
                            "activity-general-information"]

        # Iterate over the classes and check their presence
        for class_name in classes_to_check:
            element = self.find_by_class(class_name, details)
            self.assertTrue(element, f"{class_name} class not found")

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
        self.open('action:detail', future_activity.id)

        participate_button = self.find_by_class("Participate-btn")
        participate_button.click()

        # Check the messages.
        messages = self.find_by_class("alert-msg")
        except_text = 'Registration for the activity has not yet opened.'
        self.assertIn(except_text, messages.text)

    def test_create_activity(self):
        """
        Test create new activity.

        1. Count the initial activity amount
        2. LogIn
        3. Navigate to activity manage page.
        4. Click create new activity button.
        5. Fill the information and submit.
        6. Check messages.
        7. Check that the activity was created.
        """
        # Count the activity before create
        initial_count = Activity.objects.filter(owner=self.user)
        self.assertEqual(len(initial_count), 0)

        # LogIn as user_1
        self.login(self.name, self.password)

        # Navigate to activity manage page
        url = self.getUrl("action:manage")
        self.browser.get(url)

        # Click create new activity button
        create_button = self.find_by_css(".new-activity a")
        create_button.click()

        # Fill information in the fields.
        title_field = self.find_by_id("id_title")
        title_field.send_keys("TitleTestTitle")
        description_field = self.find_by_id("id_description")
        description_field.send_keys("DescriptionTestDescription")

        # Click create button for submitting
        create_button = self.find_by_css("input[type='submit'][value='Create']")
        create_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("Activity created successfully.", message.text)

        # Check that the activity was created
        activity = Activity.objects.filter(owner=self.user)
        self.assertEqual(len(activity), 1)
        self.assertEqual(activity[0].title, "TitleTestTitle")

    def test_delete_activity(self):
        """
        Test delete an activity.

        1. Create a new activity.
        2. Check the initial activity amount.
        3. LogIn.
        4. Navigate to activity manage page.
        5. Delete the activity.
        6. Check the messages.
        7. Check that the activity was deleted.
        """
        # Create an activity
        create_activity(self.user)

        # Check the activity amount
        initial_count = Activity.objects.filter(owner=self.user)
        self.assertEqual(len(initial_count), 1)

        # LogIn as user_1
        self.login(self.name, self.password)

        # Navigate to activity manage page
        url = self.getUrl("action:manage")
        self.browser.get(url)

        # Delete the activity
        delete_button = self.find_by_class("activity-delete")
        delete_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("You have successfully deleted this activity.", message.text)

        # Check that the activity was deleted.
        activity = Activity.objects.filter(owner=self.user)
        self.assertEqual(len(activity), 0)
