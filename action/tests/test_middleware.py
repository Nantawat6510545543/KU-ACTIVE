import logging

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from action.middleware import Render404Middleware, RemoveWhitespaceMiddleware


class MiddlewareTests(TestCase):
    """Test case for middleware classes."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Disable logging during unittest.
        2. Initialize a RequestFactory.
        3. Initialize a Client.
        """
        logging.disable(logging.CRITICAL)  # Disable error message during unittest
        self.factory = RequestFactory()
        self.client = Client()

    def test_render_404_middleware(self):
        """
        Test the Render404Middleware.

        1. Create an instance of Render404Middleware with HttpResponseNotFound.
        2. Make a client request to an invalid URL.
        3. Assert that accessing the middleware raises Http404 and uses the '404_error.html' template.
        """
        middleware = Render404Middleware(HttpResponseNotFound)
        response = self.client.get('/invalid')
        
        with self.assertRaises(Http404):
            updated_response = middleware(response)
            self.assertTemplateUsed(updated_response, '404_error.html')

    def test_remove_whitespace_middleware(self):
        """
        Test the RemoveWhitespaceMiddleware.

        1. Create an instance of RemoveWhitespaceMiddleware with HttpResponse.
        2. Make a request with query parameters containing leading and trailing whitespaces.
        3. Assert that the middleware removes the whitespaces from the query parameters.
        """
        middleware = RemoveWhitespaceMiddleware(HttpResponse)
        request = self.factory.get(reverse('action:index') + '/?q=%20hello%20%20%20world%20%20%20%20')
        middleware(request)

        self.assertEqual(request.GET['q'], 'hello world')

    def test_update_session_middleware(self):
        """
        Test the UpdateSessionMiddleware (not implemented).

        This method is a placeholder for testing a middleware that updates the session.
        Currently, the middleware is not implemented, so the method does not contain specific test logic.
        """
        # # Make a request with query and tag parameters
        response = self.client.get(reverse('action:index') + '?tag=categories&q=query')

        # Check if the session has been updated correctly
        session = self.client.session
        self.assertEqual(session.get('query'), 'query')
        self.assertEqual(session.get('tag'), 'categories')
