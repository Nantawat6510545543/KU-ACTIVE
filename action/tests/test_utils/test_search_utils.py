import logging

from django.urls import reverse
from django.utils import timezone
from django.test import RequestFactory, TestCase
from action.utils.search_utils import BaseSearcher
from action.tests.utils import create_activity, create_activity_status, \
    create_friend_status, create_category, create_user, quick_join


class SearchUtilsTests(TestCase):
    """Test case for the search utility functions."""

    def setUp(self) -> None:
        """
        Set up common attributes for the test methods.

        1. Disable critical logging messages during unittest.
        2. Create a RequestFactory instance.
        3. Create a user instance.
        """
        logging.disable(logging.CRITICAL)  # Disable error messages during unittest
        self.factory = RequestFactory()
        self.user = create_user()

    def test_selection(self):
        """
        Test the selection of search parameters.

        1. Make a GET request with parameters 'tag' as 'title' and 'q' as 'test'.
        2. Assert that the generated query string is 'tag=title&q=test'.
        3. Make a GET request with 'tag' as 'place' and 'q' as an empty string.
        4. Assert that the generated query string is 'tag=place&q='.
        5. Make an invalid tag case request and assert that it redirects to the index page.
        """
        response = self.client.get(reverse('action:index'), {'tag': 'title', 'q': 'test'})
        params = response.request['QUERY_STRING']
        self.assertEqual(params, 'tag=title&q=test')

        response = self.client.get(reverse('action:index'), {'tag': 'place', 'q': ''})
        params = response.request['QUERY_STRING']
        self.assertEqual(params, 'tag=place&q=')

        # Invalid tag case should redirect to index page
        response = self.client.get(reverse('action:index'), {'tag': 'invalid'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('action:index'))

    def test_title_search(self):
        """
        Test searching by title.

        1. Create a request with 'tag' as 'title' and 'q' as 'ABC'.
        2. Set the user attribute for the request.
        3. Create an activity with the title 'ABC'.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'title', 'q': 'ABC'})
        request.user = self.user
        activity_ABC = create_activity(owner=request.user, title="ABC")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_ABC)

    def test_owner_search(self):
        """
        Test searching by owner.

        1. Create a request with 'tag' as 'owner' and 'q' as 'Tester100'.
        2. Create a user with the username 'Tester100'.
        3. Set the user attribute for the request.
        4. Create an activity with the owner set to the created user.
        5. Create a BaseSearcher instance for the request.
        6. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'owner', 'q': 'Tester100'})
        request.user = create_user(username="Tester100")
        activity_tester100 = create_activity(owner=request.user, title="Test Owner")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_tester100)

    def test_categories_search(self):
        """
        Test searching by categories.

        1. Create a request with 'tag' as 'categories' and 'q' as 'Electronics'.
        2. Set the user attribute for the request.
        3. Create a category with the name 'electronics'.
        4. Create an activity with the category set to the created category.
        5. Create a BaseSearcher instance for the request.
        6. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'),
                                   {'tag': 'categories', 'q': 'Electronics'})
        request.user = self.user
        activity_categories = create_category(name='electronics')
        activity = create_activity(owner=request.user, title="Test Categories",
                                   categories=[activity_categories])

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity)

    def test_place_search(self):
        """
        Test searching by place.

        1. Create a request with 'tag' as 'place' and 'q' as 'Home'.
        2. Set the user attribute for the request.
        3. Create an activity with the place set to 'Home'.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'place', 'q': 'Home'})
        request.user = self.user
        activity_home = create_activity(owner=request.user, title="Test Place", place="Home")

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_home)

    def test_exact_date_search(self):
        """
        Test searching by exact date.

        1. Get the string representation of yesterday's date.
        2. Create a request with 'tag' as 'date_exact' and 'q' as the string representation of yesterday's date.
        3. Set the user attribute for the request.
        4. Create an activity with the start date set to yesterday.
        5. Create a BaseSearcher instance for the request.
        6. Get the first query result and assert it is the created activity.
        """
        yesterday_string = (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')

        request = self.factory.get(reverse('action:index'),
                                   {'tag': 'date_exact', 'q': yesterday_string})
        request.user = self.user
        activity_exact_date = create_activity(owner=request.user, title="Test Exact Match",
                                              start_date=timezone.now() - timezone.timedelta(
                                                  days=1))

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, activity_exact_date)

    def test_upcoming_search(self):
        """
        Test searching for upcoming activities.

        1. Create a request with 'tag' as 'upcoming'.
        2. Set the user attribute for the request.
        3. Create an activity with a start date in the future.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'upcoming'})
        request.user = self.user
        upcoming_activity = create_activity(
            owner=request.user, title="Test Upcoming",
            pub_date=timezone.now() + timezone.timedelta(days=1))

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, upcoming_activity)

    def test_popular_search(self):
        """
        Test searching for popular activities.

        1. Create a request with 'tag' as 'popular'.
        2. Set the user attribute for the request.
        3. Create three activities with varying numbers of quick joins.
        4. Create a BaseSearcher instance for the request.
        5. Get the list of query results and assert it is in the expected order.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'popular'})
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
        self.assertListEqual(query_list, [activity1, activity2, activity3])

    def test_recent_search(self):
        """
        Test searching for recent activities.

        1. Create a request with 'tag' as 'recent'.
        2. Set the user attribute for the request.
        3. Create an activity with a start date in the past.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is the created activity.
        """
        request = self.factory.get(reverse('action:index'), {'tag': 'recent'})
        request.user = self.user
        recent_activity = create_activity(
            owner=request.user, title="Test Recent",
            pub_date=timezone.now() - timezone.timedelta(seconds=10000))

        searcher = BaseSearcher(request)
        query = searcher.get_index_query().first()
        self.assertEqual(query, recent_activity)

    def test_registered_search(self):
        """
        Test searching for registered activities.

        1. Create a request with 'tag' as 'registered'.
        2. Set the user attribute for the request.
        3. Create user and activity.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is None since the user is not registered.
        6. Create an activity status for the user and activity.
        7. Get the first query result and assert it is the created activity.
        """
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

    def test_favorited_search(self):
        """
        Test searching for favorited activities.

        1. Create a request with 'tag' as 'favorited'.
        2. Set the user attribute for the request.
        3. Create user and activity.
        4. Create a BaseSearcher instance for the request.
        5. Get the first query result and assert it is None since the activity is not favorited.
        6. Create an activity status for the user and activity with favorited set to True.
        7. Get the first query result and assert it is the created activity.
        """
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

    def test_friends_search(self):
        """
        Test searching for activities joined by friends.

        1. Create a request with 'tag' as 'friend_joined'.
        2. Set the user attribute for the request.
        3. Create friend user and activity.
        4. Create a friend status with 'Accepted' status between the user and friend.
        5. Create a BaseSearcher instance for the request.
        6. Get the first query result and assert it is None since the friend has not joined.
        7. Create an activity status for the friend and activity.
        8. Get the first query result and assert it is the created activity.
        """
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

    def test_multiple_categories_search(self):
        """
        Test searching by multiple categories.

        1. Create multiple activities with different sets of categories.
        2. Test different cases where specific categories are included in the search query.
        3. Use the BaseSearcher to get the index query and check if the result matches the expected activities.
        """
        activity_categories = [create_category(f"Category{i}") for i in range(1, 11)]

        # activity1 has category 1-5, activity2 has category 3-7, activity2 has category 6-10
        activity1 = create_activity(owner=create_user("New User 1"),
                                    title="Test Multiple Categories 1",
                                    categories=activity_categories[0:5])
        activity2 = create_activity(owner=create_user("New User 2"),
                                    title="Test Multiple Categories 2",
                                    categories=activity_categories[2:7])
        activity3 = create_activity(owner=create_user("New User 3"),
                                    title="Test Multiple Categories 3",
                                    categories=activity_categories[5:10])

        # Case 1: Category 1-2 in activity1
        request = self.factory.get(reverse('action:index'), {
            'category_q': ['Category1', 'Category2'],
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity1])

        # Case 2: Category 3-5 in activity1 and activity2
        request = self.factory.get(reverse('action:index'), {
            'category_q': ['Category5', 'Category3', 'Category4'],
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity2, activity1])

        # Case 3: Category 6-7 in activity2 and activity3
        request = self.factory.get(reverse('action:index'), {
            'category_q': ['Category7', 'Category6'],
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity3, activity2])

        # Case 4: Category 8-10 in activity3
        request = self.factory.get(reverse('action:index'), {
            'category_q': ['Category10', 'Category9', 'Category8'],
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity3])

    def test_start_date_range_search(self):
        """
        Test searching by start date range.

        1. Create multiple activities with different start dates.
        2. Test different cases where the start date range is included in the search query.
        3. Use the BaseSearcher to get the index query and check if the result matches the expected activities.
        """
        activity1 = create_activity(owner=create_user("New User 1"),
                                    title="Test Last Week",
                                    start_date=timezone.now() - timezone.timedelta(days=7))
        activity2 = create_activity(owner=create_user("New User 2"),
                                    title="Test Today", start_date=timezone.now())
        activity3 = create_activity(owner=create_user("New User 3"),
                                    title="Test Next Week",
                                    start_date=timezone.now() + timezone.timedelta(days=7))

        yesterday_string = timezone.now() - timezone.timedelta(days=1)
        tomorrow_string = timezone.now() + timezone.timedelta(days=1)

        # Test start point range
        request = self.factory.get(reverse('action:index'), {
            'tag': ['date_start_point'],
            'q': yesterday_string,
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity3, activity2])

        # Test end point range
        request = self.factory.get(reverse('action:index'), {
            'tag': ['date_end_point'],
            'q': yesterday_string,
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity1])

        # Test both point range
        request = self.factory.get(reverse('action:index'), {
            'tag': ['date_start_point', 'date_end_point'],
            'q': [yesterday_string, tomorrow_string]
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity2])

    def test_multiple_tags_search(self):
        """
        Test searching with multiple tags.

        1. Create multiple activities with different titles, owners, places, and start dates.
        2. Test a case where multiple tags and queries are included in the search query.
        3. Use the BaseSearcher to get the index query and check if the result matches the expected activities.
        """
        user = create_user("Test User 1")
        activity1 = create_activity(owner=user,
                                    title="Test Tag", place="Test Place",
                                    start_date=timezone.now() - timezone.timedelta(days=1))
        activity2 = create_activity(owner=user,
                                    title="Test Tag", place="Test Place",
                                    start_date=timezone.now() - timezone.timedelta(days=10))

        last_week_string = timezone.now() - timezone.timedelta(days=7)
        request = self.factory.get(reverse('action:index'), {
            'tag': ['title', 'owner', 'place', 'date_start_point'],
            'q': ['Test Tag', 'Test User 1', 'Test place', last_week_string]
        })
        request.user = self.user

        searcher = BaseSearcher(request)
        query = list(searcher.get_index_query())
        self.assertListEqual(query, [activity1])
