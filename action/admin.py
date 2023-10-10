from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, Activity, Participation, FriendRequest


class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['activity_name']}),
        (
            'Date information',
            {'fields': ['owner', 'pub_date', 'end_date'],
             'classes': ['collapse']}),
    ]
    list_display = ('id', 'owner', 'activity_name', 'pub_date', 'end_date',
                    'is_published', 'was_published_recently',
                    'can_participate')
    list_filter = ['owner', 'end_date']
    search_fields = ['activity_name']
    ordering = ('id',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['participants', 'activity', 'participation_date']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Participation, ParticipationAdmin)
