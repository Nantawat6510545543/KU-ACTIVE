from selenium.webdriver.common.by import By

from action.tests.utils import create_user
from action.tests.end_to_end_base import EndToEndTestBase
from action.models import Activity


class ActivityTestsE2E(EndToEndTestBase):
    """Test case for the views related to activity creation."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Define a username and password.
        2. Create a user with the defined username and password.
        """
        super().setUp()
        self.name_1 = 'user1'
        self.password_1 = 'pass1'
        self.user_1 = create_user(self.name_1, self.password_1)

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
        initial_count = Activity.objects.filter(owner=self.user_1)
        self.assertEqual(len(initial_count), 0)

        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to activity manage page
        url = self.getUrl("action:manage")
        self.browser.get(url)

        # Click create new activity button
        create_button = self.browser.find_element(By.CSS_SELECTOR, ".new-activity a")
        create_button.click()

        # Fill information in the fields.
        title_field = self.browser.find_element(By.ID, "id_title")
        title_field.send_keys("TitleTestTitle")
        description_field = self.browser.find_element(By.ID, "id_description")
        description_field.send_keys("DescriptionTestDescription")

        # Click create button for submit
        create_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
        create_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("Activity created successfully.", message.text)

        # Check that the activity was created
        activity = Activity.objects.filter(owner=self.user_1)
        self.assertEqual(len(activity), 1)
        self.assertEqual(activity[0].title, "TitleTestTitle")