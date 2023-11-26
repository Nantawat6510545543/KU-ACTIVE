from django.test import TestCase
from action.tests import utils


class ActivityStatusTestCase(TestCase):
    """Test case for the ActivityStatus model."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create a user instance
        2. Create an activity instance with the created user as the owner.
        3. Create an activity_status instance with the created user as the participant.
        """
        user = utils.create_user()
        activity = utils.create_activity(owner=user)
        self.activity_status = utils.create_activity_status(participants=user,
                                                            activity=activity)

    def test_activity_status_attributes(self):
        """
        Test the attributes of the ActivityStatus model.

        1. Get the created activity_status instance.
        2. Check if the participants attribute is equal to the owner of the activity.
        3. Check if is_participated is True.
        4. Check if is_favorited is False.
        """
        activity_status = self.activity_status

        self.assertEqual(activity_status.participants,
                         activity_status.activity.owner)
        self.assertTrue(activity_status.is_participated)
        self.assertFalse(activity_status.is_favorited)
