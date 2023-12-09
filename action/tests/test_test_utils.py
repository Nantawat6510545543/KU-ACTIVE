from django.test import TestCase
from django.utils import timezone

from .utils import create_user, create_category, create_activity, \
    create_activity_status, create_friend_status, quick_join, create_request


class TestUtilsTest(TestCase):
    """Test case for the utility functions in the tests directory."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create an owner user.
        2. Create a category.
        3. Create an activity with the owner and category.
        4. Create a participant user.
        """
        self.owner = create_user(username='activity_owner', password='password', email='owner@example.com')
        self.category = create_category(name='Test Category')
        self.activity = create_activity(owner=self.owner, title='Test Activity', categories=[self.category])
        self.participant_user = create_user(username='participant_user', password='password', email='participant@example.com')

    def test_create_activity(self):
        """
        Test the create_activity utility function.

        1. Create an activity using create_activity.
        2. Check if the activity attributes match the expected values.
        """
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
        """
        Test the create_activity_status utility function.

        1. Create an activity_status using create_activity_status.
        2. Check if is_participated is True and is_favorited is False.
        """
        activity_status = create_activity_status(
            participants=self.participant_user, activity=self.activity)
        self.assertTrue(activity_status.is_participated)
        self.assertFalse(activity_status.is_favorited)

    def test_create_friend_status(self):
        """
        Test the create_friend_status utility function.

        1. Create friend_status1 without specifying request_status.
        2. Check if request_status is None and is_friend is False.

        3. Create friend_status2 with request_status 'Accepted'.
        4. Check if request_status is 'Accepted' and is_friend is True.

        5. Create friend_status3 with request_status 'Declined'.
        6. Check if request_status is 'Declined' and is_friend is False.
        """
        sender = create_user(username='sender_user', password='password', email='sender@example.com')
        receiver = create_user(username='receiver_user', password='password', email='receiver@example.com')
        friend_status1 = create_friend_status(sender=sender, receiver=receiver)
        self.assertIsNone(friend_status1.request_status)
        self.assertFalse(friend_status1.is_friend)

        friend_status2 = create_friend_status(sender=sender, receiver=receiver, request_status='Accepted')
        self.assertEqual(friend_status2.request_status, 'Accepted')
        self.assertTrue(friend_status2.is_friend)

    def test_quick_join(self):
        """
        Test the quick_join utility function.

        1. Call quick_join with a participant username.
        2. Check if the participant is added to the activity.
        """
        quick_join(participants="Test Quick Join", activity=self.activity)
        self.assertEqual(self.activity.participants[0].username, "Test Quick Join")

    def test_create_request(self):
        """
        Test the create_request utility function.

        1. Create a request with the action:index view and no arguments.
        2. Check if the request user is the owner user.
        """
        request = create_request(view='action:index', args=[], user=self.owner)
        self.assertEqual(request.user, self.owner)
