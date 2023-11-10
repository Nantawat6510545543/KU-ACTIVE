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


class ActivityManageViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_manage_activity_redirect(self):
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_redirect(self):
        available_activity = create_activity(self.user)
        url = reverse('action:delete_activity', args=(available_activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
