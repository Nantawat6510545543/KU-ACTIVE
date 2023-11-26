import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from action.tests.utils import create_social_app


class EndToEndTestBase(StaticLiveServerTestCase):
    """End-to-end Base class"""

    browser = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = FirefoxOptions()
        options.add_argument("--headless")
        cls.browser = Firefox(options=options)
        cls.browser.implicitly_wait(30)
        cls.browser.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        create_social_app()

    def open(self, view, web_id):
        self.url = self.getUrl(view, (web_id,))
        self.browser.get(self.url)

    def find_by_class(self, class_name, element=None):
        if element is not None:
            return element.find_element(By.CLASS_NAME, class_name)
        return self.browser.find_element(By.CLASS_NAME, class_name)

    def getUrl(self, view, args=None):
        if args is None:
            return self.live_server_url + reverse(view)
        return self.live_server_url + reverse(view, args=args)

    def login(self, username, password):
        self.browser.get(self.getUrl("login"))

        user_field = self.browser.find_element(By.NAME, "username")
        user_field.send_keys(username)

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)
