from django.contrib import admin

from .models import Activity, Tag, Participation, FriendRequest, User
from .forms import ActivityAdminForm


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    fieldsets = [
        (None, {'fields': ['activity_name']}),
        ('Date information',
         {'fields': ['owner', 'pub_date', 'end_date', 'activity_date',
                     'description', 'place'],
          'classes': ['collapse']}),
        ('Tags', {'fields': ['tags'], 'classes': ['wide']}),
    ]
    list_display = ('id', 'owner', 'activity_name', 'pub_date', 'end_date',
                    'is_published', 'was_published_recently',
                    'can_participate')
    list_filter = ['owner', 'end_date']
    search_fields = ['activity_name']
    ordering = ('id',)
    filter_horizontal = ('tags',)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'bio']


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['participants', 'activity', 'participation_date']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Activity, ActivityAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
