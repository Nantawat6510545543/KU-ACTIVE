from django.test import TestCase
from action.models import User, Activity, ActivityStatus


class ActivityStatusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="testpassword")
        self.activity = Activity.objects.create(owner=self.user,
                                                title="Test Activity",
                                                description="Test Description")
        self.activity_status = ActivityStatus.objects.create(
            participants=self.user, activity=self.activity)

    def test_activity_status_participants(self):
        self.assertEqual(self.activity_status.participants, self.user)

    def test_activity_status_activity(self):
        self.assertEqual(self.activity_status.activity, self.activity)

    def test_activity_status_is_participated(self):
        self.assertFalse(self.activity_status.is_participated)

    def test_activity_status_is_favorited(self):
        self.assertFalse(self.activity_status.is_favorited)
