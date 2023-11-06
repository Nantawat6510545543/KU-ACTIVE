from abc import ABC, abstractmethod

from django.http import HttpRequest


class BaseMiddleware(ABC):
    def __init__(self, get_response):
        self.get_response = get_response

    @abstractmethod
    def __call__(self, request: HttpRequest):
        pass


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
