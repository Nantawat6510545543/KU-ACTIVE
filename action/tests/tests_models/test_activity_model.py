from action.tests.utils import Tester
from django.utils import timezone


class ActivityModelTest(Tester):

    def setUp(self):
        super().setUp()
        self.user1 = self.create_user('tester1')
        self.user2 = self.create_user('tester2')
        self.tag1 = self.create_tag(name="Tag1")
        self.tag2 = self.create_tag(name="Tag2")

        time = timezone.now()

        self.activity_data = {
            'owner': self.user1,
            'start_date': time,
            'last_date': time + timezone.timedelta(days=1),
            'pub_date': time + timezone.timedelta(days=2),
            'end_date': time + timezone.timedelta(days=3),
            'participant_limit': 1,
            'tags': [self.tag1, self.tag2]
        }

        self.activity = self.create_activity(**self.activity_data)

    def test_activity_attributes(self):
        activity = self.activity
        data = self.activity_data

        self.assertEqual(activity.owner, data['owner'])
        self.assertEqual(activity.start_date, data['start_date'])
        self.assertEqual(activity.last_date, data['last_date'])
        self.assertEqual(activity.pub_date, data['pub_date'])
        self.assertEqual(activity.end_date, data['end_date'])
        self.assertEqual(activity.participant_limit, data['participant_limit'])
        self.assertCountEqual(data['tags'], activity.tags.all())
