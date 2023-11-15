from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils import timezone

from action.models import Activity, ActivityStatus

class BaseSearcher:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.query = request.GET.get('q')
        self.tag = request.GET.get('tag')
        self.user = request.user

        self.activities = Activity.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')

    def set_searcher(self):
        match self.tag:
            case None: searcher = IndexSearcher(self.request)
            case 'title': searcher = TitleSearcher(self.request)
            case 'owner': searcher = OwnerSearcher(self.request)
            case 'date': searcher = DateSearcher(self.request)
            case 'tag': searcher = TagSearcher(self.request)
            case 'place': searcher = PlaceSearcher(self.request)
            case 'upcoming': searcher = UpcomingSearcher(self.request)
            case 'popular': searcher = PopularSearcher(self.request)
            case 'recent': searcher = RecentSearcher(self.request)
            case 'friend_joined': searcher = FriendJoinedSearcher(self.request)
            case 'registered': searcher = RegisteredSearcher(self.request)
            case 'favorited': searcher = FavoritedSearcher(self.request)
            case _: raise ValueError("Invalid Tag")
        self.searcher = searcher

    def get_index_query(self):
        self.set_searcher()
        return self.searcher.get_index_query()


class IndexSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities


class TitleSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(title__icontains=self.query)


class OwnerSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(owner__username__icontains=self.query)


class DateSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(date__icontains=self.query)


class TagSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(tags__name__icontains=self.query)


class PlaceSearcher(BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(place__icontains=self.query)


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
        now = timezone.datetime.now()
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

        return self.activities.filter(Q(activity__in=user_activity_status))


class RegisteredSearcher(LoginRequiredMixin, BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(Q(id__in=self.user.participated_activity))


class FavoritedSearcher(LoginRequiredMixin, BaseSearcher):
    def get_index_query(self):
        return self.activities.filter(Q(id__in=self.user.favorited_activity))
