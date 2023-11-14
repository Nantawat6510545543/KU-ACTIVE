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


class FriendStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        user_data_2 = {"email": "test2@example.com"}
        self.user_2 = create_user(username="Jane", password="abc", **user_data_2)

