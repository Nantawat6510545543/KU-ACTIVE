from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from ..models import ActivityStatus
from ..utils import activity_status_utils as as_utils


@login_required
def participate(request, activity_id: int):
    activity_status: ActivityStatus = as_utils.fetch_activity_status(request,
                                                                     activity_id)

    if activity_status.is_participated:
        messages.info(request, "You are already participating.")
    else:
        activity_status.is_participated = True
        activity_status.save()
        messages.success(request, "You have successfully participated.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def leave(request, activity_id: int):
    activity_status: ActivityStatus = as_utils.fetch_activity_status(request,
                                                                     activity_id)

    if activity_status.is_participated:
        activity_status.is_participated = False
        activity_status.save()
        messages.success(request, "You have left this activity.")
    else:
        messages.info(request,
                      "You are not currently participating in this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def favorite(request, activity_id: int):
    activity_status: ActivityStatus = as_utils.fetch_activity_status(request,
                                                                     activity_id)

    if activity_status.is_favorited:
        messages.info(request, "You have already favorited this activity.")
    else:
        activity_status.is_favorited = True
        activity_status.save()
        messages.success(request,
                         "You have successfully favorited this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def unfavorite(request, activity_id: int):
    activity_status: ActivityStatus = as_utils.fetch_activity_status(request,
                                                                     activity_id)

    if activity_status.is_favorited:
        activity_status.is_favorited = False
        activity_status.save()
        messages.success(request, "You have un-favorited this activity.")
    else:
        messages.info(request,
                      "You have not currently favorite this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))