from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from action.middleware import Render404Middleware, RemoveWhitespaceMiddleware, UpdateSessionMiddleware


class MiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_render_404_middleware_debug_true(self):
        middleware = Render404Middleware(HttpResponseNotFound)
        request = self.factory.get('/invalid')
        with self.settings(DEBUG=True):
            with self.assertRaises(Http404):
                middleware(request)

    def test_render_404_middleware_debug_false(self):
        middleware = Render404Middleware(HttpResponseNotFound)
        request  = self.factory.get('/invalid')
        with self.settings(DEBUG=False):
            with self.assertRaises(Http404):
                response = middleware(request)
                self.assertTemplateUsed(response, '404_error.html')

    def test_remove_whitespace_middleware(self):
        middleware = RemoveWhitespaceMiddleware(HttpResponse)
        request = self.factory.get(reverse('action:index') + '/?q=%20hello%20%20%20world%20%20%20%20')
        middleware(request)

        self.assertEqual(request.GET['q'], 'hello world')

    def test_update_session_middleware(self):
        # # Make a request with query and tag parameters
        response = self.client.get(reverse('action:index') + '?tag=categories&q=query')

        # Check if the session has been updated correctly
        session = self.client.session
        self.assertEqual(session.get('query'), 'query')
        self.assertEqual(session.get('tag'), 'categories')