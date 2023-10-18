from allauth.socialaccount.models import SocialApp

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from decouple import config

from mysite.settings import SITE_ID, SITE_NAME, SITE_DOMAIN


class Command(BaseCommand):
    help = 'Setup site and social app in the Django admin'

    def handle(self, *args, **options):
        try:
            # Delete the existing "example.com" site
            Site.objects.filter(domain='example.com').delete()

            # Create or update the Site
            site, created = Site.objects.get_or_create(
                id = SITE_ID,
                defaults = {
                    'name': SITE_NAME,
                    'domain': SITE_DOMAIN,
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS('Site created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Site loaded successfully.'))

            # Create or update the SocialApp
            social_app, social_app_created = SocialApp.objects.get_or_create(
                provider = 'google',
                defaults = {
                    'name': 'Login with Google OAuth',
                    'client_id': config('GOOGLE_OAUTH_CLIENT_ID'),
                    'secret': config('GOOGLE_OAUTH_SECRET_KEY'),
                },
            )

            social_app.sites.add(site)

            if social_app_created:
                self.stdout.write(self.style.SUCCESS('Google OAuth SocialApp created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Google OAuth SocialApp loaded successfully.'))

        except IntegrityError:
            self.stdout.write(self.style.WARNING('Error: Site or SocialApp with this ID already exists.'))
