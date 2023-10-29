from django.views import generic

from .. import utils


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        return utils.get_index_queryset(self.request)
