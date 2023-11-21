from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest
from django.utils import timezone
from urllib.parse import parse_qs

from action.models import Activity, ActivityStatus


def get_query_dict(request: HttpRequest):
    """
    Custom function that return dictionary of 
    {request.GET.get('tag'): request.GET.get('q')}
    """
    # print(f"{request.META['QUERY_STRING'] =}")
    params = parse_qs(request.META['QUERY_STRING'], keep_blank_values=True)
    values_q = params.get('q', [])
    values_tag = request.GET.getlist('tag')

    return dict(zip(values_tag, values_q))


#  Checkbox works differently than searchbox, so custom function is needed
def get_categories_list(request: HttpRequest):
    values_category_q = request.GET.getlist('category_q')
    return values_category_q


class BaseSearcher:  # TODO Dependency Injection!!!
    def __init__(self, request: HttpRequest):
        self.request = request
        self.user = request.user
        self.query_dict = get_query_dict(request)
        self.tag = None

        self.activities = Activity.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')

    def set_searcher(self):
        match self.tag:
            case None: searcher = IndexSearcher
            case 'title': searcher = TitleSearcher
            case 'owner': searcher = OwnerSearcher
            case 'date_start_point': searcher = DateSearcher
            case 'date_end_point': searcher = DateSearcher
            case 'date_exact': searcher = DateSearcher
            case 'categories': searcher = CategoriesSearcher
            case 'category_list': searcher = CategoryListSearcher
            case 'place': searcher = PlaceSearcher
            case 'upcoming': searcher = UpcomingSearcher
            case 'popular': searcher = PopularSearcher
            case 'recent': searcher = RecentSearcher
            case 'friend_joined': searcher = FriendJoinedSearcher
            case 'registered': searcher = RegisteredSearcher
            case 'favorited': searcher = FavoritedSearcher
            case _: raise ValueError(f"Invalid Tag: {self.tag}")
        self.searcher = searcher(self.request)

    # Note: "is None" does not work with empty string/list/dict
    def get_index_query(self):
        # print(f"{self.query_dict =}")
        category_dict = get_categories_list(self.request)

        if category_dict:
            self.activities = self.get_aaa()
        # Case where query is None (not empty string), for tags without 'q' as url parameters.
        # Tags: upcoming, popular, recent, friend_joined, registered, favorited tags.
        if not self.query_dict:
            # This returns the last value of tag=, assuming there's only one tag= in url
            self.tag = self.request.GET.get('tag')
            self.set_searcher()
            return self.searcher.get_index_query()

        # Case where query exists
        for each_tag, each_query in self.query_dict.items():
            if not each_query:
                continue  # Skip if query is an empty string

            self.tag = each_tag
            self.set_searcher()

            # print(f"{self.tag=}")
            # print(f"{each_query=}")
            # print(f"{self.searcher=}")

            self.activities &= self.searcher.get_index_query()

        return self.activities


    def get_aaa(self):
        self.tag = 'category_list'
        self.set_searcher()

        category_list = get_categories_list(self.request)
        for each_category in category_list:
            self.activities &= self.searcher.get_index_query()
        return self.activities


class IndexSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities


class TitleSearcher(BaseSearcher):
    def get_index_query(self):
        title_query = self.query_dict.get('title', None)
        return self.activities.filter(title__icontains=title_query)


class OwnerSearcher(BaseSearcher):
    def get_index_query(self):
        owner_query = self.query_dict.get('owner', None)
        return self.activities.filter(owner__username__icontains=owner_query)


class DateSearcher(BaseSearcher):
    def get_index_query(self):
        # Set the value to None if not specified, using empty string
        # (default for empty url params) wil causes invalid datetime format
        start_point = self.query_dict.get('date_start_point', None)
        end_point = self.query_dict.get('date_end_point', None)
        exact_point = self.query_dict.get('date_exact', None)

        filtered_activity = self.activities

        if exact_point:
            exact_date = datetime.strptime(exact_point, '%Y-%m-%dT%H:%M').date()
            filtered_activity &= self.activities.filter(start_date__date=exact_date)
            return filtered_activity

        if start_point:
            filtered_activity &= self.activities.filter(start_date__gte=start_point)
        
        if end_point:
            filtered_activity &= self.activities.filter(start_date__lte=end_point)

        return filtered_activity


class CategoriesSearcher(BaseSearcher):
    def get_index_query(self):
        categories_query = self.query_dict.get('categories', None)
        return self.activities.filter(categories__name__iexact=categories_query)


class CategoryListSearcher(BaseSearcher):  # Currently doesn't work
    def get_index_query(self):
        category_list = get_categories_list(self.request)
        for each_category in category_list:
            if each_category:
                self.activities &= self.activities.filter(categories__name__iexact=each_category)
        return self.activities


class PlaceSearcher(BaseSearcher):
    def get_index_query(self):
        place_query = self.query_dict.get('place', None)
        return self.activities.filter(place__icontains=place_query)


class UpcomingSearcher(BaseSearcher):
    def get_index_query(self):
        now = timezone.now()
        delay = timezone.timedelta(days=7)
        activities = Activity.objects.order_by('-pub_date')
        return activities.filter(pub_date__range=(now, now + delay))


class PopularSearcher(BaseSearcher):
    def get_index_query(self):
        activities = self.activities.filter(activity__is_participated=True)
        # Add a temporary column and filter by it (temp_participant_count), descending
        activities = self.activities.annotate(
            temp_participant_count=Count('activity__participants'))
        activities = activities.order_by('-temp_participant_count')
        return activities


class RecentSearcher(BaseSearcher):
    def get_index_query(self):
        now = timezone.now()
        delay = timezone.timedelta(days=7)
        activities = Activity.objects.order_by('-pub_date')
        return activities.filter(pub_date__range=(now - delay, now))


class FriendJoinedSearcher(LoginRequiredMixin, BaseSearcher):
    def get_index_query(self):
        # Can't directly call activity__participants_is_participated,
        # not supported by Django ManyToOneRel. So it's broken into two queries
        # First call participants_is_participate, then filter by activity

        # Get ActivityStatus objects for your friends and is_participated=True
        user_activity_status = ActivityStatus.objects.filter(
            participants__in=self.user.friends, is_participated=True)

        return self.activities.filter(activity__in=user_activity_status).distinct()


class RegisteredSearcher(LoginRequiredMixin, BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(id__in=self.user.participated_activity)


class FavoritedSearcher(LoginRequiredMixin, BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(id__in=self.user.favorited_activity)