"""
This module is for helper functions.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone

from decouple import config
import pyrebase

from .models import Activity, ActivityStatus, FriendStatus, User

# Define a global variable to store the Firebase instance
_firebase_instance = None

def get_firebase_instance():
    global _firebase_instance
    if _firebase_instance is None:
        _firebase_instance = pyrebase.initialize_app({
            "apiKey": config('FIREBASE_API_KEY'),
            "authDomain": config('FIREBASE_AUTH_DOMAIN'),
            "projectId": config('FIREBASE_PROJECT_ID'),
            "storageBucket": config('FIREBASE_STORAGE_BUCKET'),
            "messagingSenderId": config('FIREBASE_MESSAGING_SENDER_ID'),
            "appId": config('FIREBASE_APP_ID'),
            "measurementId": config('FIREBASE_MEASUREMENT_ID'),
            "databaseURL": config('FIREBASE_DATABASE_URL')
        })
    return _firebase_instance


# TODO write less stupid code
# TODO maybe try Filter/Meditator Design Pattern
# TODO refactor "Sort" option to separate function
# TODO save user's sort/filter settings by using session
# TODO add support for multiple criteria queries

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


@login_required
def fetch_activity_status(request, activity_id: int) -> ActivityStatus:
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user

    # TODO factor out the activity part
    # if not activity.can_participate():
    #     messages.error(request, "You can't participate in this activity.")
    #     return redirect("action:index")

    try:
        activity_status = ActivityStatus.objects. \
            get(participants=user, activity=activity)

    except ActivityStatus.DoesNotExist:
        activity_status = ActivityStatus.objects. \
            create(participants=user, activity=activity)

    return activity_status


@login_required
def fetch_friend_status(request, friend_id: int) -> FriendStatus:
    user1 = request.user
    user2 = User.objects.get(id=friend_id)

    try:
        friend_status = FriendStatus.objects.get(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1))

    # This might cause bug idk
    except FriendStatus.DoesNotExist:
        friend_status = FriendStatus.objects. \
            create(sender=user1, receiver=user2)

    return friend_status
