from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from action.models import Activity, ActivityStatus


@login_required
def fetch_activity_status(request, activity_id: int) -> ActivityStatus:
    """
    Fetch the activity status for the current user and the specified activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity for which to fetch the status.

    Returns:
        ActivityStatus: The activity status for the current user and activity.

    Note:
        This function is intended to be used as a view or in conjunction with views that
        require the user to be authenticated. It fetches the activity status for the current
        user and the specified activity, creating a new status if it does not exist.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user

    try:
        activity_status = ActivityStatus.objects. \
            get(participants=user, activity=activity)

    except ActivityStatus.DoesNotExist:
        activity_status = ActivityStatus.objects. \
            create(participants=user, activity=activity)

    return activity_status
