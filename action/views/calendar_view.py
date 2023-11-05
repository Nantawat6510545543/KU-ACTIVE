from django.views import generic

from action import utils


class CalendarView(generic.ListView):
    template_name = 'action/calendar.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        return utils.ActivityFilterer(self.request).get_index_queryset()
