from django.contrib.auth.decorators import login_required
from django.db.models import Q

from action.models import FriendStatus, User


@login_required
def fetch_friend_status(request, friend_id: int) -> FriendStatus:
    """
    Fetch the friendship status between the authenticated user and the specified friend.

    If a friendship status does not exist, it will be created.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The user ID of the friend.

    Returns:
        FriendStatus: The friendship status between the authenticated user and the friend.
    """
    user1 = request.user
    user2 = User.objects.get(id=friend_id)

    try:
        friend_status = FriendStatus.objects.get(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1))

    except FriendStatus.DoesNotExist:
        friend_status = FriendStatus.objects. \
            create(sender=user1, receiver=user2)

    return friend_status
