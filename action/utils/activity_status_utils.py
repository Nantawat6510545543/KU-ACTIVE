from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from ..models import Activity, ActivityStatus


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
