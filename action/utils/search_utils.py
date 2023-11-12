from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils import timezone

from action.models import Activity, ActivityStatus


def get_tag_query(request: HttpRequest):
    now = timezone.now()
    delay = timezone.timedelta(1)

    query = request.GET.get('q')
    user = request.user

    tag_query = {
        'title': Q(title__icontains=query),
        'owner': Q(owner__username__icontains=query),
        'date': Q(date__icontains=query),
        'tag': Q(tags__name__icontains=query),
        'place': Q(place__icontains=query),
        'upcoming': Q(pub_date__range=(now, now + delay)),
        'popular': Q(),
        'recent': Q(pub_date__range=(now - delay, now))
    }

    if user.is_authenticated:
        # Can't directly call activity__participants_is_participated,
        # not supported by Django ManyToOneRel. So it's broken into two queries
        # First call participants_is_participate, then filter by activity

        # Get ActivityStatus objects for your friends and is_participated=True
        user_activity_status = ActivityStatus.objects.filter(
            participants__in=user.friends, is_participated=True)

        tag_query.update({
            # Filter 'friend_joined' by related Activity objects
            'friend_joined': Q(activity__in=user_activity_status),
            'registered': Q(id__in=user.participated_activity),
            'favorited': Q(id__in=user.favorited_activity)
        })

    return tag_query


def get_index_queryset(request: HttpRequest):
    tag = request.GET.get('tag')
    tag_query = get_tag_query(request)

    if tag is not None and tag not in tag_query:
        raise ValueError("Invalid Tag")

    activities = Activity.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')

    match tag:
        case 'popular':        
            activities = activities.filter(activity__is_participated=True)
            # Add a temporary column and filter by it (temp_participant_count), descending
            activities = activities.annotate(
                temp_participant_count=Count('activity__participants'))
            activities = activities.order_by('-temp_participant_count')
            return activities

        case 'upcoming' | 'recent':
            activities = Activity.objects.order_by('-pub_date')

    if tag:
        filters = tag_query[tag]
        activities = activities.filter(filters).distinct()
    return activities
