import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from action.tests.utils import create_social_app


class EndToEndTestBase(StaticLiveServerTestCase):
    """Base class for end-to-end tests using Selenium and Firefox."""

    browser = None

    def setUpClass(cls):
        """
        Set up the Firefox browser for headless mode.

        1. Create Firefox options with the "--headless" argument.
        2. Initialize the Firefox browser with the created options.
        """
        super().setUpClass()
        options = FirefoxOptions()
        options.add_argument("--headless")
        cls.browser = Firefox(options=options)
        cls.browser.implicitly_wait(30)
        cls.browser.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls):
        """Close the Firefox browser."""
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        """Set up a social app using `create_social_app`."""
        create_social_app()

    def open(self, view, web_id):
        """
        Open a specific view with optional arguments.

        1. Get the URL for the specified view and arguments.
        2. Navigate to the URL using the Firefox browser.
        """
        self.url = self.getUrl(view, (web_id,))
        self.browser.get(self.url)

    def find_by_class(self, class_name, element=None):
        """
        Find an element by its class name.

        Args:
            - `class_name`: The class name of the element to find.
            - `element`: Optional parent element to search within.

        Returns:
            - The found element.
        """
        if element is not None:
            return element.find_element(By.CLASS_NAME, class_name)
        return self.browser.find_element(By.CLASS_NAME, class_name)

    def getUrl(self, view, args=None):
        """
        Get the URL for a given view and arguments.

        Args:
            - `view`: The view name.
            - `args`: Optional arguments for the view.

        Returns:
            - The constructed URL.
        """
        if args is None:
            return self.live_server_url + reverse(view)
        return self.live_server_url + reverse(view, args=args)

    def login(self, username, password):
        """
        Perform login with the provided username and password.

        1. Navigate to the login page.
        2. Find the username and password fields.
        3. Enter the provided username and password.
        4. Press the RETURN key.
        5. Sleep for 1 second to allow the login process to complete.
        """
        self.browser.get(self.getUrl("login"))

        user_field = self.browser.find_element(By.NAME, "username")
        user_field.send_keys(username)

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)
