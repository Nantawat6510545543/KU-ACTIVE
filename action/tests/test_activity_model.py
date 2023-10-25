from .utils import Tester
from django.utils import timezone


class ActivityModelTest(Tester):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.tag1 = self.create_tag(name="Tag1")
        self.tag2 = self.create_tag(name="Tag2")

        time = timezone.now()

        self.activity_data = {
            'owner': self.user,
            'date': time,
            'pub_date': time,
            'end_date': time + timezone.timedelta(days=1),
            'participant_limit': 10,
            'tags': [self.tag1, self.tag2]
        }

        self.activity = self.create_activity(**self.activity_data)

    def test_activity_attributes(self):
        activity = self.activity
        data = self.activity_data

        self.assertEqual(activity.owner, data['owner'])
        self.assertEqual(activity.date, data['date'])
        self.assertEqual(activity.pub_date, data['pub_date'])
        self.assertEqual(activity.end_date, data['end_date'])
        self.assertEqual(activity.participant_limit, data['participant_limit'])
        self.assertCountEqual(data['tags'], activity.tags.all())
