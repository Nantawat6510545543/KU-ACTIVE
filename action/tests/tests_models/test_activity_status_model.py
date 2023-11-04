from action.tests.utils import Tester


class ActivityStatusTestCase(Tester):
    def setUp(self):
        super().setUp()
        user = self.create_user()
        activity = self.create_activity(owner=user)
        self.activity_status = self.create_activity_status(participants=user,
                                                           activity=activity)

    def test_activity_status_attributes(self):
        activity_status = self.activity_status

        self.assertEqual(activity_status.participants,
                         activity_status.activity.owner)
        self.assertTrue(activity_status.is_participated)
        self.assertFalse(activity_status.is_favorited)
