from django.test import TestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialApp
from decouple import config


class GoogleAllauthTestCase(TestCase):
    def setUp(self):
        # Create a SocialApp for Google if it doesn't exist
        social_app, social_app_created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Login with Google OAuth',
                'client_id': config('GOOGLE_OAUTH_CLIENT_ID'),
                'secret': config('GOOGLE_OAUTH_SECRET_KEY'),
            },
        )

    def test_google_social_app_creation(self):
        """
        Ensure that the SocialApp for Google was created successfully
        """
        google_app = SocialApp.objects.get(provider='google')
        self.assertEqual(google_app.name, 'Login with Google OAuth')
        self.assertEqual(google_app.client_id,
                         config('GOOGLE_OAUTH_CLIENT_ID'))
        self.assertEqual(google_app.secret, config('GOOGLE_OAUTH_SECRET_KEY'))

    def test_google_login_page(self):
        """
        Test that the Google login page is accessible.
        """
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_google_logout_page(self):
        """
        Test that the Google logout page redirects appropriately.
        """
        response = self.client.post(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')
