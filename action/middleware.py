from abc import ABC, abstractmethod

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from mysite.settings import DEBUG


class BaseMiddleware(ABC):
    """Abstract base class for middleware."""

    def __init__(self, get_response):
        """
        Initialize the middleware with the next middleware or view function.

        Args:
            get_response (Callable): The next middleware or view function in the request-response chain.
        """
        self.get_response = get_response

    @abstractmethod
    def __call__(self, request: HttpRequest):
        """
        Process the request and handle 404 responses.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response.
        """
        pass


class Render404Middleware(BaseMiddleware):
    """Middleware for rendering a custom 404 page."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and handle 404 responses.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response.
        """
        response = self.get_response(request)

        if response.status_code != 404:  # For other status code
            return response

        # Use default 404 with DEBUG = True, otherwise use custom one
        if DEBUG:
            raise Http404()
        return render(request, '404_error.html', status=404)


class RemoveWhitespaceMiddleware(BaseMiddleware):
    """Middleware for removing whitespace from query parameters."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request by removing whitespace from query parameters.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response.
        """
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
    """Middleware for updating session variables based on query parameters."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request by updating session variables based on query parameters.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response.
        """
        query = request.GET.get('q')
        tag = request.GET.get('tag')

        request.session['query'] = query or None

        if tag not in [None, 'upcoming', 'popular', 'recent']:
            request.session['tag'] = tag

        response = self.get_response(request)
        return response
