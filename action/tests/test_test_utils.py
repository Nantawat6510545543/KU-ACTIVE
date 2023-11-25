from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .utils import create_user, create_category, create_activity, \
    create_activity_status, create_friend_status, quick_join, create_request


class TestUtilsTest(TestCase):

    def setUp(self):
        self.owner = create_user(username='activity_owner', password='password', email='owner@example.com')
        self.category = create_category(name='Test Category')
        self.activity = create_activity(owner=self.owner, title='Test Activity', categories=[self.category])
        self.participant_user = create_user(username='participant_user', password='password', email='participant@example.com')

    def test_create_activity(self):
        activity = create_activity(self.owner)
        now = timezone.now().date()

        self.assertEqual(activity.title, "Test")
        self.assertEqual(activity.owner, self.owner)
        self.assertEqual(activity.pub_date.date(), now)
        self.assertEqual(activity.end_date.date(), now + timezone.timedelta(days=1))
        self.assertEqual(activity.start_date.date(), now + timezone.timedelta(days=2))
        self.assertEqual(activity.last_date.date(), now + timezone.timedelta(days=3))
        self.assertEqual(activity.description, "")
        self.assertIsNone(activity.place)
        self.assertIsNone(activity.full_description)
        self.assertIsNone(activity.participant_limit)
        self.assertListEqual(list(activity.categories.all()), [])

    def test_create_activity_status(self):
        activity_status = create_activity_status(
            participants=self.participant_user, activity=self.activity)
        self.assertTrue(activity_status.is_participated)
        self.assertFalse(activity_status.is_favorited)

    def test_create_friend_status(self):
        sender = create_user(username='sender_user', password='password', email='sender@example.com')
        receiver = create_user(username='receiver_user', password='password', email='receiver@example.com')
        friend_status1 = create_friend_status(sender=sender, receiver=receiver)
        self.assertIsNone(friend_status1.request_status)
        self.assertFalse(friend_status1.is_friend)

        friend_status2 = create_friend_status(sender=sender, receiver=receiver, request_status='Pending')
        self.assertEqual(friend_status2.request_status, 'Pending')

    def test_quick_join(self):
        quick_join(participants="Test Quick Join", activity=self.activity)
        self.assertEqual(self.activity.participants[0].username, "Test Quick Join")

    def test_create_request(self):
        request = create_request(view='action:index', args=[], user=self.owner)
        self.assertEqual(request.user, self.owner)
