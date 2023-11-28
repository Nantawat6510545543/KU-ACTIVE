from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from action.calendar import update_event
from action.utils.calendar import user_is_login_with_google


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    """View for displaying a calendar of activities."""

    template_name = 'action/calendar.html'

    def get(self, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests for the calendar view.

        If the user is not logged in with a Google account, show a warning message and redirect to the Google login page.
        If the user has a Google social account, proceed with the regular view logic.

        Args:
            - `*args`: Additional positional arguments.
            - `**kwargs`: Additional keyword arguments.

        Returns:
            - `HttpResponse`: The HTTP response for rendering the calendar template.
        """
        if user_is_login_with_google(self.request.user):
            for each_activity in self.request.user.participated_activity:
                update_event(self.request, each_activity.id)
        else:
            # If the user doesn't have a Google social account, Redirect to the Google login page
            messages.warning(self.request, "Please login to Google to use the calendar feature.")
            # return render(self.request, 'socialaccount/login.html', {'provider': 'google'})

        # Proceed with the regular view logic
        return super(CalendarView, self).get(*args, **kwargs)
