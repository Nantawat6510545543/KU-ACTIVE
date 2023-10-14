from django.test import TestCase
from django.utils import timezone
from action.models import User, Activity


class ActivityModelTest(TestCase):
    """
    Test case for the Activity model.

    This class contains test methods to verify
    the attributes and behavior of the Activity model.
    """

    def setUp(self):
        """
        Set up a User instance to be used as the owner for Activity instances.
        """
        # Create a User instance
        self.user = User(username="testuser")
        self.user.save()

    def test_owner_attribute(self):
        """
        Test the owner attribute of the Activity model.
        """
        # Create an Activity instance with a specific owner
        activity = Activity(owner=self.user)
        activity.save()

        self.assertEqual(activity.owner, self.user)

    def test_activity_name_attribute(self):
        """
        Test the activity_name attribute of the Activity model.
        """
        activity = Activity(owner=self.user, title="Test Activity")
        activity.save()
        self.assertEqual(activity.title, "Test Activity")

    def test_pub_date_attribute(self):
        """
        Test the pub_date attribute of the Activity model.
        """
        pub_date = timezone.now()
        activity = Activity(owner=self.user, pub_date=pub_date)
        activity.save()
        self.assertEqual(activity.pub_date, pub_date)

    def test_end_date_attribute(self):
        """
        Test the end_date attribute of the Activity model.
        """
        end_date = timezone.now() + timezone.timedelta(days=30)
        activity = Activity(owner=self.user, end_date=end_date)
        activity.save()
        self.assertEqual(activity.end_date, end_date)

    def test_date_attribute(self):
        """
        Test the activity_date attribute of the Activity model.
        """
        activity_date = timezone.now()
        activity = Activity(owner=self.user, date=activity_date)
        activity.save()
        self.assertEqual(activity.date, activity_date)

    def test_description_attribute(self):
        """
        Test the description attribute of the Activity model.
        """
        activity = Activity(owner=self.user, description="Test Description")
        activity.save()
        self.assertEqual(activity.description, "Test Description")

    def test_place_attribute(self):
        """
        Test the place attribute of the Activity model.
        """
        activity = Activity(owner=self.user, place="Test Place")
        activity.save()
        self.assertEqual(activity.place, "Test Place")
