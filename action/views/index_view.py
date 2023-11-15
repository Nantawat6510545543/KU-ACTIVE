from django.shortcuts import redirect
from django.views import generic

from action.utils import search_utils

TAG_OPTIONS = [
    ('title', 'Title'),
    ('owner', 'Owner'),
    ('tag', 'Tag'),
    ('place', 'Place'),
    ('start_date', 'Date'),
]

# Some tag requires login
REGISTERED_TAG_LIST = ['registered', 'favorited', 'friend_joined']


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag')

        # Check if tag in register_tag_list and user is logged in
        if tag in REGISTERED_TAG_LIST and not request.user.is_authenticated:
            return redirect('login')

        # Continue with the regular behavior of the view
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return search_utils.get_index_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the tag options to the context
        context['tags'] = TAG_OPTIONS
        return context
