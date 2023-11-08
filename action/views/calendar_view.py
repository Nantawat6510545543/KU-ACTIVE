from django.views import generic

from action.utils import search_utils


class CalendarView(generic.ListView):
    template_name = 'action/calendar.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        return search_utils.get_index_queryset(self.request)
