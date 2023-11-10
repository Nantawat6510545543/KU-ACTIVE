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


class ActivityDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()


