import logging

from django.urls import reverse
from django.utils import timezone
from django.test import RequestFactory, TestCase
from action.utils.search_utils import BaseSearcher
from action.tests.utils import create_activity, create_activity_status, create_friend_status, create_tag, create_user, quick_join


class SearchUtilsTests(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)  # Disable error message during unittest
        self.factory = RequestFactory()
        self.user = create_user()
        # self.tags = [create_tag(f"Tag{i}") for i in range(1, 6)]

    def test_selection(self):
        response = self.client.get(reverse('action:index'), {'tag': 'title', 'q': 'test'})
        params = response.request['QUERY_STRING']
        self.assertEqual(params, 'tag=title&q=test')

        response = self.client.get(reverse('action:index'), {'tag': 'place', 'q': ''})
        params = response.request['QUERY_STRING']
        self.assertEqual(params, 'tag=place&q=')

        with self.assertRaises(ValueError):  # Invalid Tag Case
            response = self.client.get(reverse('action:index'), {'tag': 'invalid'})

    def test_title_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'title', 'q': 'ABC'})
        request.user = self.user  # Do not delete any kind of this line, it will break the code
        activityABC = create_activity(owner=request.user, title="ABC")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activityABC)

    def test_owner_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'owner', 'q': 'Tester100'})
        request.user = create_user(username="Tester100")
        activity_tester100 = create_activity(owner=request.user, title="Test Owner")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_tester100)

    # TODO change tag to categories + add multiple tag support????
    def test_categories_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'categories', 'q': 'Electronics'})
        request.user = self.user
        # this should be categories='Electronics' instead
        activity_tag = create_tag(name='electronics')
        activity_categories = create_activity(owner=request.user, title="Test Categories", tags=[activity_tag])

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_categories)

    def test_place_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'place', 'q': 'Home'})
        request.user = self.user
        activity_home = create_activity(owner=request.user, title="Test Place", place="Home")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_home)

    def test_upcoming_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'upcoming'})
        request.user = self.user
        upcoming_activity = create_activity(
            owner=request.user, title="Test Upcoming", pub_date=timezone.now() + timezone.timedelta(days=1))

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, upcoming_activity)

    def test_popular_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'recent'})
        request.user = self.user

        activity1 = create_activity(owner=request.user, title="1")
        activity2 = create_activity(owner=request.user, title="2")
        activity3 = create_activity(owner=request.user, title="3")

        quick_join("user1", activity1)
        quick_join("user2", activity1)
        quick_join("user3", activity1)
        quick_join("user4", activity2)
        quick_join("user5", activity2)
        quick_join("user6", activity3)

        searcher = BaseSearcher(request)
        query_list = list(searcher.get_index_query())
        self.assertListEqual(query_list, [activity3, activity2, activity1])

    def test_recent_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'recent'})
        request.user = self.user
        recent_activity = create_activity(
            owner=request.user, title="Test Recent", 
            pub_date=timezone.now() - timezone.timedelta(seconds=10000))
        
        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, recent_activity)

    def test_registered_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'registered'})
        request.user = self.user
        creator = create_user(username="Creator")
        activity = create_activity(owner=creator, title="Test Registered Tag")

        # not registered case
        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertIsNone(query, "Registered should be None, no registered yet")

        # registered case
        create_activity_status(request.user, activity)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity)

    def test_favorited_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'favorited'})
        request.user = self.user
        creator = create_user(username="Creator")
        activity = create_activity(owner=creator, title="Test Favorited Tag")

        # not favorited case
        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertIsNone(query, "Favorite should be None, no favorite yet")

        # favorited case
        create_activity_status(request.user, activity, is_favorited=True)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity)

    def test_friends_tag(self):
        request = self.factory.get(reverse('action:index'), {'tag': 'friend_joined'})
        request.user = self.user
        friend = create_user(username="Friend")
        activity = create_activity(owner=self.user, title="Test Friend_joined Tag")

        # not friend case
        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertIsNone(query, "Friend should be None, no friend yet")

        # friend case, not joined
        create_friend_status(request.user, friend, request_status="Accepted")
        query = searcher.get_index_query().first()
        self.assertIsNone(query, "Friend exists, but didn't join yet")

        # friend case, joined
        create_activity_status(friend, activity)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity)