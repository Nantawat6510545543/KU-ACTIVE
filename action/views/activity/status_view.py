from allauth.socialaccount.models import SocialToken
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from googleapiclient.errors import HttpError

from action.models import ActivityStatus, Activity
from action import utils


# TODO modify so it fits open/closed principle using State pattern
@login_required
def participate(request, activity_id: int):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity_status: ActivityStatus = \
        utils.fetch_activity_status(request, activity_id)

    if not activity.is_published():
        messages.info(request,
                      "Registration for the activity has not yet opened.")
    elif not activity.can_participate():
        messages.info(request,
                      "This activity can no longer be participated in.")
    elif activity_status.is_participated:
        messages.info(request, "You are already participating.")
    else:
        try:
            utils.create_event(request, activity_id)
        except SocialToken.DoesNotExist:  # If user have email but not google accounts
            pass
        except HttpError:
            messages.info(request,
                          "Calendar is not working, please Login again.")

        activity_status.is_participated = True
        activity_status.save()
        messages.success(request, "You have successfully participated.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def leave(request, activity_id: int):
    activity_status: ActivityStatus = utils.fetch_activity_status(request,
                                                                  activity_id)

    if activity_status.is_participated:
        activity_status.is_participated = False
        activity_status.save()
        messages.success(request, "You have left this activity.")
        try:
            utils.remove_event(request, activity_id)
        except SocialToken.DoesNotExist:  # If user have email but not google accounts
            pass
        except HttpError:
            messages.info(request,
                          "Calendar is not working, please Login again.")

    else:
        messages.info(request,
                      "You are not currently participating in this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def favorite(request, activity_id: int):
    activity_status: ActivityStatus = utils.fetch_activity_status(request,
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
    activity_status: ActivityStatus = utils.fetch_activity_status(request,
                                                                  activity_id)

    if activity_status.is_favorited:
        activity_status.is_favorited = False
        activity_status.save()
        messages.success(request, "You have unfavorited this activity.")
    else:
        messages.info(request,
                      "You have not currently favorite this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))
