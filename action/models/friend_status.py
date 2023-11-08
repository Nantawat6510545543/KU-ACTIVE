from django.db import models
from .user import User


class FriendStatus(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="receiver")

    request_status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                                      null=True, default=None)
    is_friend = models.BooleanField(default=False)
