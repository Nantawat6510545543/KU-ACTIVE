from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from action.utils.calendar import user_is_login_with_google


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    """View for displaying a calendar of activities."""

    template_name = 'action/calendar.html'

    def get(self, *args, **kwargs):
        if not user_is_login_with_google(self.request):
            # If the user doesn't have a Google social account, Redirect to the Google login page
            messages.warning(self.request, "Please login to Google to use the calendar feature.")

            # return render(self.request, 'socialaccount/login.html', {'provider': 'google'})

        # If the user already has a Google social account, proceed with the regular view logic
        return super(CalendarView, self).get(*args, **kwargs)
