from action.tests.utils import Tester
from django.utils import timezone


class ActivityModelTest(Tester):

    def setUp(self):
        super().setUp()
        self.user_list = [self.create_user(f'tester{i}') for i in range(1, 4)]
        self.tag_list = [self.create_tag(name=f'Tag{i}') for i in range(1, 3)]

        time = timezone.now()

        self.activity_data = {
            'owner': self.user_list[0],
            'start_date': time,
            'last_date': time + timezone.timedelta(days=1),
            'pub_date': time + timezone.timedelta(days=2),
            'end_date': time + timezone.timedelta(days=3),
            'participant_limit': 1,
            'tags': self.tag_list
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
        self.assertCountEqual(activity.tags.all(), data['tags'])

    def test_participant_count(self):
        self.assertEqual(self.activity.participant_count, 0)

        activity_status = []
        for i in range(3):
            activity_status.append(
                self.create_activity_status(self.user_list[i], self.activity))
            self.assertEqual(self.activity.participant_count, i + 1)

        count = self.activity.participant_count - 1

        for i in range(3):
            activity_status[i].delete()
            self.assertEqual(self.activity.participant_count, count - i)
