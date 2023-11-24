from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    """View for displaying a calendar of activities."""

    template_name = 'action/calendar.html'
