from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest
from django.utils import timezone
from urllib.parse import parse_qs

from action.models import Activity, ActivityStatus


def get_query_dict(request: HttpRequest):
    """
    Extract and return a dictionary mapping tag names to their corresponding query values.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary mapping tag values to their corresponding query values.
    """
    params = parse_qs(request.META['QUERY_STRING'], keep_blank_values=True)
    values_q = params.get('q', [])
    values_tag = request.GET.getlist('tag')

    return dict(zip(values_tag, values_q))


def get_categories_list(request: HttpRequest):
    """
    Get a list of category values from the request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        list: A list of category values.
    """
    values_category_q = request.GET.getlist('category_q')
    return values_category_q

# TODO refactor
class BaseSearcher:
    """Base class for searching activities based on various criteria."""

    def __init__(self, request: HttpRequest):
        """
        Initialize a BaseSearcher instance with the given HTTP request.

        Args:
            request (HttpRequest): The HTTP request object.

        Attributes:
            request (HttpRequest): The HTTP request object associated with the instance.
            user (User): The authenticated user associated with the request.
            query_dict (dict): A dictionary mapping tag names to their corresponding query values.
            tag (str): The current tag being processed, initially set to None.
            activities (QuerySet): The base queryset of activities filtered by publication date.
        """
        self.request = request
        self.user = request.user
        self.query_dict = get_query_dict(request)
        self.tag = None

        self.activities = Activity.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')

    def set_searcher(self):
        """
        Set the searcher instance based on the current tag.

        Raises:
            ValueError: If an invalid tag is encountered.
        """
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

    def get_index_query(self):
        """
        Get the final queryset based on the applied filters.

        Returns:
            QuerySet: The final queryset of activities.
        """
        category_list = get_categories_list(self.request)

        # Case where there's a list of category
        if category_list:
            self.tag = 'category_list'
            self.set_searcher()
            self.activities = self.searcher.get_index_query()

        # Case where query is None (not empty string), for tags without 'q' as url parameters.
        # Tags: upcoming, popular, recent, friend_joined, registered, favorited tags.
        if not self.query_dict and not category_list:
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
            self.activities &= self.searcher.get_index_query()

        return self.activities


class IndexSearcher(BaseSearcher):
    """Searcher for the default index view."""

    def get_index_query(self):
        """
        Return the base queryset of activities.

        Returns:
            QuerySet: The base queryset of activities.
        """
        return self.activities


class TitleSearcher(BaseSearcher):
    """Searcher for filtering activities by title."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by title.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        title_query = self.query_dict.get('title', None)
        return self.activities.filter(title__icontains=title_query)


class OwnerSearcher(BaseSearcher):
    """Searcher for filtering activities by owner."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by owner.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        owner_query = self.query_dict.get('owner', None)
        return self.activities.filter(owner__username__icontains=owner_query)


class DateSearcher(BaseSearcher):
    """Searcher for filtering activities by date."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by date.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        # Set the value to None if not specified, using an empty string
        # (default for empty URL params) will cause an invalid datetime format
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
    """Searcher for filtering activities by categories."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by categories.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        categories_query = self.query_dict.get('categories', None)
        return self.activities.filter(categories__name__iexact=categories_query)


class CategoryListSearcher(BaseSearcher):
    """Searcher for filtering activities by a list of categories."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by a list of categories.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        category_list = get_categories_list(self.request)
        for each_category in category_list:
            if each_category:
                self.activities &= self.activities.filter(categories__name__iexact=each_category)
        return self.activities


class PlaceSearcher(BaseSearcher):
    """Searcher for filtering activities by place."""

    def get_index_query(self):
        """
        Return the queryset of activities filtered by place.

        Returns:
            QuerySet: The filtered queryset of activities.
        """
        place_query = self.query_dict.get('place', None)
        return self.activities.filter(place__icontains=place_query)


class UpcomingSearcher(BaseSearcher):
    """Searcher for retrieving upcoming activities."""

    def get_index_query(self):
        """
        Return the queryset of upcoming activities.

        Returns:
            QuerySet: The queryset of upcoming activities.
        """
        now = timezone.now()
        delay = timezone.timedelta(days=7)
        activities = Activity.objects.order_by('-pub_date')
        return activities.filter(pub_date__range=(now, now + delay))


class PopularSearcher(BaseSearcher):
    """Searcher for retrieving popular activities."""

    def get_index_query(self):
        """
        Return the queryset of popular activities.

        Returns:
            QuerySet: The queryset of popular activities.
        """
        self.activities = self.activities.filter(activity__is_participated=True)

        # Add a temporary column and filter by it (temp_participant_count), descending
        self.activities = self.activities.annotate(
            temp_participant_count=Count('activity__participants'))
        self.activities = self.activities.order_by('-temp_participant_count')
        return self.activities


class RecentSearcher(BaseSearcher):
    """Searcher for retrieving recent activities."""

    def get_index_query(self):
        """
        Return the queryset of recent activities.

        Returns:
            QuerySet: The queryset of recent activities.
        """
        now = timezone.now()
        delay = timezone.timedelta(days=7)
        activities = Activity.objects.order_by('-pub_date')
        return activities.filter(pub_date__range=(now - delay, now))


class FriendJoinedSearcher(LoginRequiredMixin, BaseSearcher):
    """Searcher for retrieving activities joined by friends."""

    def get_index_query(self):
        """
        Return the queryset of activities joined by friends.

        Returns:
            QuerySet: The queryset of activities joined by friends.
        """
        # Can't directly call activity__participants_is_participated,
        # not supported by Django ManyToOneRel. So it's broken into two queries
        # First call participants_is_participate, then filter by activity

        # Get ActivityStatus objects for your friends and is_participated=True
        user_activity_status = ActivityStatus.objects.filter(
            participants__in=self.user.friends, is_participated=True)

        return self.activities.filter(activity__in=user_activity_status).distinct()


class RegisteredSearcher(LoginRequiredMixin, BaseSearcher):
    """Searcher for retrieving registered activities."""

    def get_index_query(self):
        """
        Return the queryset of registered activities.

        Returns:
            QuerySet: The queryset of registered activities.
        """
        return self.activities.filter(id__in=self.user.participated_activity)


class FavoritedSearcher(LoginRequiredMixin, BaseSearcher):
    """Searcher for retrieving favorited activities."""

    def get_index_query(self):
        """
        Return the queryset of favorited activities.

        Returns:
            QuerySet: The queryset of favorited activities.
        """
        return self.activities.filter(id__in=self.user.favorited_activity)
