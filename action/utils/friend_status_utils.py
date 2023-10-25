from django.contrib.auth.decorators import login_required
from django.db.models import Q

from ..models import FriendStatus, User


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
