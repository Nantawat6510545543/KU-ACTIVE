from django.views import generic

from ..utils import search_utils as su


class CalendarView(generic.ListView):
    template_name = 'action/calendar.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        return su.get_index_queryset(self.request)
