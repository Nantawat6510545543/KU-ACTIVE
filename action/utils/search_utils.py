from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils import timezone

from action.models import Activity, ActivityStatus


def get_index_queryset(request: HttpRequest):
    query = request.GET.get('q')
    tag = request.GET.getlist('tag')
    activities = Activity.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    filters = Q()  # Create an empty query

    for each_tag in tag:
        match each_tag:
            case 'title':
                filters |= Q(title__icontains=query)
            case 'owner':
                filters |= Q(owner__username__icontains=query)
            # date currently doesn't work
            case 'date':
                filters |= Q(date__icontains=query)
            case 'tag':
                filters |= Q(tags__name__icontains=query)
            case 'place':
                filters |= Q(place__icontains=query)

            # TODO extract method
            case 'registered':
                filters |= Q(id__in=request.user.participated_activity)

            case 'favorited':
                filters |= Q(id__in=request.user.favorited_activity)

            case 'friend_joined':
                # Can't directly call activity__participants_is_participated,
                # not supported by Django ManyToOneRel. So it's broken into two queries
                # First call participants_is_participate, then filter by activity

                # Get ActivityStatus objects for your friends and is_participated=True
                activity_status = ActivityStatus.objects.filter(participants__in=request.user.friends, is_participated=True)

                # Filter by related Activity objects
                filters |= Q(activity__in=activity_status)

            case 'upcoming':
                # TODO Default is one day before after activity, consider reassigning it or separating it
                activities = Activity.objects.order_by('-pub_date')
                filters |= Q(pub_date__range=(timezone.now(), timezone.now() + timezone.timedelta(1)))
            case 'popular':
                activities = activities.annotate(temp_participant_count=Count('activity'))
                activities = activities.order_by('-temp_participant_count')
            case 'recent':
                # TODO Default is one day before the activity, consider reassigning it or separate it
                activities = Activity.objects.order_by('-pub_date')
                filters |= Q(pub_date__range=(timezone.now() - timezone.timedelta(1), timezone.now()))

    activities = activities.filter(filters)
    return activities
