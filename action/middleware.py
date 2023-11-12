from abc import ABC, abstractmethod

from django.http import HttpRequest
from django.shortcuts import render

from mysite.settings import DEBUG


class BaseMiddleware(ABC):
    def __init__(self, get_response):
        self.get_response = get_response

    @abstractmethod
    def __call__(self, request: HttpRequest):
        pass


class Render404Middleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        # TODO detailed error make DEBUG = True
        # Check if the response has a 404 status code
        if response.status_code == 404:
            return render(request, '404_error.html', status=404)

        return response


class RemoveWhitespaceMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        # Get the query parameters from the request
        query = request.GET.get('q')
        if query:
            query = " ".join(query.split())

        # Update the query parameters in the request
        request.GET = request.GET.copy()
        request.GET['q'] = query or ''

        response = self.get_response(request)
        return response


class UpdateSessionMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        query = request.GET.get('q')
        tag = request.GET.get('tag')

        request.session['query'] = query or None

        # TODO This is a quick fix, will fix in detail later
        if tag not in [None, 'upcoming', 'popular', 'recent']:
            request.session['tag'] = tag

        response = self.get_response(request)
        return response
