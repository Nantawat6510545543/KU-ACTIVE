from django.shortcuts import redirect
from django.views import generic

from action.models import Category
from action.utils.search_utils import BaseSearcher

TAG_OPTIONS = [
    ('title', 'Title'),
    ('owner', 'Owner'),
    ('categories', 'Categories'),
    ('place', 'Place'),
    ('exact_date', 'Exact Date'),
]

# Some tag requires login
REGISTERED_TAG_LIST = ['registered', 'favorited', 'friend_joined']


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag')

        # User must log in to access registered tag list
        if tag in REGISTERED_TAG_LIST and not request.user.is_authenticated:
            return redirect('login')

        # Continue with the regular behavior of the view
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        searcher = BaseSearcher(self.request)
        return searcher.get_index_query()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the tag options to the context
        context['categories'] = Category.objects.all()
        context['tags'] = TAG_OPTIONS
        return context
