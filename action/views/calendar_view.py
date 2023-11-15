from django.views import generic

class CalendarView(generic.TemplateView):
    template_name = 'action/calendar.html'
