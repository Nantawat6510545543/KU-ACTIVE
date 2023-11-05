from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils import timezone

from action.models import Activity, ActivityStatus


class ActivityFilterer:
    def __init__(self, request: HttpRequest):
        # Can't directly call activity__participants_is_participated,
        # not supported by Django ManyToOneRel. So it's broken into two queries
        # First call participants_is_participate, then filter by activity

        self.query = request.GET.get('q')
        self.tag = request.GET.get('tag')
        now = timezone.now()
        delay = timezone.timedelta(1)
        self.tag_handler = {
            'title': Q(title__icontains=self.query),
            'owner': Q(owner__username__icontains=self.query),
            'date': Q(date__icontains=self.query),
            'tag': Q(tags__name__icontains=self.query),
            'place': Q(place__icontains=self.query),
            'upcoming': Q(pub_date__range=(now, now + delay)),
            'popular': Q(),
            'recent': Q(pub_date__range=(now - delay, now))
        }

        user = request.user
        if user.is_authenticated:
            # Get ActivityStatus objects for your friends and is_participated=True
            user_activity_status = ActivityStatus.objects.filter(
                participants__in=user.friends, is_participated=True)
            self.tag_handler.update({
                # Filter 'friend_joined' by related Activity objects
                'friend_joined': Q(activity__in=user_activity_status),
                'registered': Q(id__in=user.participated_activity),
                'favorited': Q(id__in=user.favorited_activity)
            })

    def get_index_queryset(self):
        if self.tag is not None and self.tag not in self.tag_handler:
            raise ValueError("Invalid Tag")

        activities = Activity.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')

        match self.tag:
            case 'popular':
                activities = activities.annotate(
                    temp_participant_count=Count('activity'))
                activities = activities.order_by('-temp_participant_count')
                return activities
            case 'upcoming' | 'recent':
                activities = Activity.objects.order_by('-pub_date')

        if self.tag:
            filters = self.tag_handler[self.tag]
            activities = activities.filter(filters)
        return activities
