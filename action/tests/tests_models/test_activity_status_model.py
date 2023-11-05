from django.test import TestCase
from action.tests import utils


class ActivityStatusTestCase(TestCase):
    def setUp(self):
        user = utils.create_user()
        activity = utils.create_activity(owner=user)
        self.activity_status = utils.create_activity_status(participants=user,
                                                           activity=activity)

    def test_activity_status_attributes(self):
        activity_status = self.activity_status

        self.assertEqual(activity_status.participants,
                         activity_status.activity.owner)
        self.assertTrue(activity_status.is_participated)
        self.assertFalse(activity_status.is_favorited)
