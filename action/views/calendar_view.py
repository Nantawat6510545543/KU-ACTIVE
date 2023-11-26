from allauth.socialaccount.models import SocialAccount

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    """View for displaying a calendar of activities."""

    template_name = 'action/calendar.html'

    def get(self, *args, **kwargs):
        try:
            # Check if the user has a Google social account
            SocialAccount.objects.get(user=self.request.user, provider='google')
        except SocialAccount.DoesNotExist:
            # If the user doesn't have a Google social account, Redirect to the Google login page
            messages.warning(self.request, "Please login to Google to use the calendar feature.")

            # return render(self.request, 'socialaccount/login.html', {'provider': 'google'})

        # If the user already has a Google social account, proceed with the regular view logic
        return super(CalendarView, self).get(*args, **kwargs)
