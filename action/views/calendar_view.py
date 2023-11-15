from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'action/calendar.html'
