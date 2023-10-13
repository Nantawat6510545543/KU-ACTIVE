from django.contrib import admin

from .models import Activity, FriendRequest, Tag, ActivityStatus, User
from .forms import ActivityAdminForm


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    fieldsets = [
        ('Required', {'fields': ['title', 'owner', 'description', 'place', 'picture']}),
        ('Date information',
         {'fields': ['pub_date', 'end_date', 'date'],
          'classes': ['collapse']}),
        ('Optional', {'fields': ['participant_limit', 'full_description', 'background_picture'],
                      'classes': ['wide']}),
        ('Tags', {'fields': ['tags'], 'classes': ['wide']}),
    ]
    list_display = ('id', 'owner', 'title', 'pub_date', 'end_date',
                    'is_published', 'was_published_recently',
                    'can_participate')
    list_filter = ['owner', 'end_date']
    search_fields = ['title']
    ordering = ('id',)
    filter_horizontal = ('tags',)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'bio']


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']


class ActivityStatusAdmin(admin.ModelAdmin):
    list_display = ['participants', 'activity', 'participation_date']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Activity, ActivityAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
