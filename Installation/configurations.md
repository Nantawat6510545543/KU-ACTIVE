## Configuration - [sample.env](sample.env) File

To set up your project, you'll need to configure the `sample.env` file. Depending on your intended usage, follow these steps to update the necessary variables:

### For Google OAuth Integration

If you plan to use Google OAuth, make sure to replace the following variables in your `sample.env` file:

- `GOOGLE_OAUTH_CLIENT_ID`: Replace this with your own Google OAuth Client ID.
- `GOOGLE_OAUTH_SECRET_KEY`: Replace this with your own Google OAuth Secret Key.

You can obtain your Google OAuth credentials by referring to the [Google OAuth Key + Secret guide](https://support.google.com/cloud/answer/6158849).

Please note that if you choose not to configure these settings, you can still use basic login functionality, but OAuth features will be unavailable.

After completing the installation, if you wish to update your credentials, modify the .env file and execute the following code:
```
python manage.py setup_oauth
```

### For Online Database Integration

If you're using an online database, ensure that you update the following variable in your `sample.env` file:

- `DATABASE_URL`: Replace this with your own database credentials. Obtain your Neon database URL by following the instructions provided in the [Connect with psql guide](https://neon.tech/docs/connect/query-with-psql-editor).



