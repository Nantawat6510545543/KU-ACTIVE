import datetime

import django.test
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from action.models import *
from action.tests import utils
from mysite import settings
from action.tests.utils import *


class ActivityEditViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_view_activity_edit(self):
        available_activity = create_activity(self.user)
        url = reverse('action:edit', args=(available_activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
