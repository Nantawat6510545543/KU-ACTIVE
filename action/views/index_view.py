from django.views import generic

from .. import utils

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

    def get_queryset(self):
        return utils.get_index_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the tag options to the context
        context['tags'] = TAG_OPTIONS
        utils.update_sessions(self.request)
        return context