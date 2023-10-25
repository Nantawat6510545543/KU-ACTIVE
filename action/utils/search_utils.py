from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils import timezone

from ..models import Activity


def get_index_queryset(request: HttpRequest):
    query = request.GET.get('q')
    criteria = request.GET.getlist('criteria')
    activities = Activity.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    filters = Q()  # Create an empty query

    for each_criteria in criteria:
        match each_criteria:
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
            case 'upcoming':
                # TODO Default is one day before after activity, consider reassigning it or separate it
                activities = Activity.objects.order_by('-pub_date')
                filters |= Q(pub_date__range=(timezone.now(), timezone.now() + timezone.timedelta(1)))
            case 'popularity':
                activities = activities.annotate(temp_participant_count=Count('activity'))
                activities = activities.order_by('-temp_participant_count')
            case 'recent':
                # TODO Default is one day before the activity, consider reassigning it or separate it
                activities = Activity.objects.order_by('-pub_date')
                filters |= Q(pub_date__range=(timezone.now() - timezone.timedelta(1), timezone.now()))

    activities = activities.filter(filters)
    return activities
