from django.contrib import admin

from .models import Activity, ActivityStatus, FriendStatus, Tag, User
from .forms import ActivityAdminForm


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    fieldsets = [
        ('Required', {
            'fields': [
                'title', 'owner', 'description', 'place', 'picture'
            ]
        }),

        ('Date information', {
            'fields': [
                'pub_date', 'end_date', 'date'
            ],
            'classes': [
                'collapse'
            ]
        }),

        ('Optional', {
            'fields': [
                'participant_limit', 'full_description', 'background_picture'
            ],
            'classes': ['wide']
        }),

        ('Tags', {
            'fields': ['tags'],
            'classes': ['wide']
        }),
    ]

    list_display = (
        'id', 'owner', 'title', 'pub_date', 'end_date',
        'is_published', 'was_published_recently', 'can_participate')

    list_filter = ['owner', 'end_date']
    search_fields = ['title']
    ordering = ('id',)
    filter_horizontal = ('tags',)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'bio']


class FriendStatusAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'request_status', 'is_friend']

    def save_model(self, request, obj, form, change):
        if obj.request_status == "Accepted":
            obj.is_friend = True
        else:
            obj.is_friend = False
        obj.save()


class ActivityStatusAdmin(admin.ModelAdmin):
    list_display = [
        'participants', 'activity', 'is_participated',
        'is_favorited', 'participation_date'
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Activity, ActivityAdmin)
admin.site.register(FriendStatus, FriendStatusAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
