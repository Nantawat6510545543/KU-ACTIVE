from django.shortcuts import redirect
from django.views import generic

from action import utils

TAG_OPTIONS = [
    ('title', 'Title'),
    ('owner', 'Owner'),
    ('tag', 'Tag'),
    ('place', 'Place'),
    ('date', 'Date'),
]


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    # TODO refactor
    def get(self, request, *args, **kwargs):
        tag_list = request.GET.getlist('tag')
        # Some tag requires login
        registered_tag_list = ['registered', 'favorited', 'friend_joined']

        # Check if tag in register_tag_list
        tag_in_registered_tag_list = any(each_tag in registered_tag_list for each_tag in tag_list)

        if tag_in_registered_tag_list and not request.user.is_authenticated:
            return redirect('login')

        # Continue with the regular behavior of the view
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return utils.get_index_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the tag options to the context
        context['tags'] = TAG_OPTIONS
        utils.update_sessions(self.request)
        return context