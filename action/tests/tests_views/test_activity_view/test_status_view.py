from datetime import timedelta

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from mysite import settings
from action.models import *
from action.tests import utils
from action.tests.utils import *
from action.forms.activity_form import *


class ActivityStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)
        self.activity = create_activity(self.user)

    # TODO: Tests not work
    # def test_guest_participate(self):
    #     """
    #     Guest should not be able to participate.
    #     Should be redirected.
    #     """
    #     url = reverse('action:participate', args=(self.activity.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_self_participate(self):
    #     """
    #     Activity owner should be able to participate their own activity.
    #     """
    #     self.client.force_login(self.user)
    #     url = reverse('action:participate', args=(self.activity.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
