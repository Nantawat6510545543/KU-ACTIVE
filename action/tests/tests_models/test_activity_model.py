from django.test import TestCase
from action.tests import utils
from django.utils import timezone


class ActivityModelTest(TestCase):

    def setUp(self):
        self.user_list = [utils.create_user(f'tester{i}') for i in range(1, 4)]
        self.category_list = [utils.create_category(name=f'Category{i}') for i in range(1, 3)]

        time = timezone.now()

        self.activity_data = {
            'title': "activity01",
            'owner': self.user_list[0],
            'pub_date': time,
            'end_date': time + timezone.timedelta(days=1),
            'start_date': time + timezone.timedelta(days=2),
            'last_date': time + timezone.timedelta(days=3),
            'place': '',
            'description': "this is activity",
            'full_description': '',
            'participant_limit': 5,
            'categories': self.category_list
        }

        self.activity = utils.create_activity(**self.activity_data)

    def test_activity_attributes(self):
        activity = self.activity
        data = self.activity_data

        # Check every attribute of model object equal to a manual object
        for key, value in data.items():
            if key == 'categories':  # modify activity.tags to list
                self.assertEqual(list(activity.categories.all()), value)
            else:
                # getattr loops over all attributes in an object (model)
                self.assertEqual(getattr(activity, key), value)

    def test_participant_count(self):
        self.assertEqual(self.activity.participant_count, 0)

        activity_status = []
        for i in range(3):
            activity_status.append(
                utils.create_activity_status(self.user_list[i], self.activity))
            self.assertEqual(self.activity.participant_count, i + 1)

        count = self.activity.participant_count - 1

        for i in range(3):
            activity_status[i].delete()
            self.assertEqual(self.activity.participant_count, count - i)

    def test_time_remain_registration(self):
        # open
        delay = timezone.timedelta(days=1) + timezone.timedelta(hours=1)
        future_time = timezone.now() + delay
        self.activity.end_date = future_time
        time_dif = abs(self.activity.time_remain - delay)
        self.assertLessEqual(time_dif, timezone.timedelta(seconds=1))

        # closed
        past_time = timezone.now() - timezone.timedelta(days=1)
        self.activity.end_date = past_time
        self.assertEqual(self.activity.time_remain,
                         timezone.timedelta(seconds=0))

    def test_remaining_space(self):
        self.activity.participant_limit = 0
        self.assertEqual(self.activity.remaining_space, None)

        self.activity.participant_limit = 5
        self.assertEqual(self.activity.remaining_space, 5)

        for i in range(3):
            utils.create_activity_status(self.user_list[i], self.activity)
            self.assertEqual(self.activity.remaining_space, 4 - i)

    def test_was_published_recently(self):
        # True
        future_time = timezone.now() - timezone.timedelta(hours=12)
        self.activity.pub_date = future_time
        self.assertTrue(self.activity.was_published_recently())

        # False
        past_time = timezone.now() - timezone.timedelta(days=2)
        self.activity.pub_date = past_time
        self.assertFalse(self.activity.was_published_recently())

    def test_is_published_true(self):
        # True
        past_time = timezone.now() - timezone.timedelta(days=2)
        self.activity.pub_date = past_time
        self.assertTrue(self.activity.is_published())

        # False
        future_time = timezone.now() + timezone.timedelta(hours=12)
        self.activity.pub_date = future_time
        self.assertFalse(self.activity.is_published())

    def test_can_participate(self):
        # True: within time range with space
        self.assertTrue(self.activity.can_participate())

        # True: within time range no space limit:
        self.activity.participant_limit = None
        self.assertTrue(self.activity.can_participate())

        # False: no space:
        self.activity.participant_limit = 3
        activity_status = []
        for i in range(3):
            activity_status.append(
                utils.create_activity_status(self.user_list[i], self.activity))
        self.assertFalse(self.activity.can_participate())

        # False: outside time range
        self.activity.participant_limit = None
        self.activity.pub_date = timezone.now() - timezone.timedelta(hours=2)
        self.activity.end_date = timezone.now() - timezone.timedelta(hours=1)
        self.assertFalse(self.activity.can_participate())
