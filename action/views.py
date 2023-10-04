from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        """
        return
