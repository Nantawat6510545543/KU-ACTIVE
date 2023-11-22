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
    by = By
    keys = Keys

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

    def getUrl(self, view, args=None):
        if args is None:
            return self.live_server_url + reverse(view)
        return self.live_server_url + reverse(view, args=args)

    def login(self, username, password):
        self.browser.get(self.getUrl("login"))

        user_field = self.browser.find_element(self.by.NAME, "username")
        user_field.send_keys(username)

        password_field = self.browser.find_element(self.by.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(self.keys.RETURN)

        time.sleep(1)

        # self.client.login(username=self.username, password=self.password)
        # cookie = self.client.cookies["sessionid"]
        # self.browser.add_cookie(
        #     {
        #         "name": "sessionid",
        #         "value": cookie.value,
        #         "secure": False,
        #         "path": "/",
        #     }
        # )
        # self.browser.refresh()
