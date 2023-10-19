## Installation Instructions

### Configuration - [sample.env](sample.env) File

To set up your project, you'll need to configure the `sample.env` file. Depending on your intended usage, follow these steps to update the necessary variables:

#### For Google OAuth Integration

If you plan to use Google OAuth, make sure to replace the following variables in your `sample.env` file:

- `GOOGLE_OAUTH_CLIENT_ID`: Replace this with your own Google OAuth Client ID.
- `GOOGLE_OAUTH_SECRET_KEY`: Replace this with your own Google OAuth Secret Key.

You can obtain your Google OAuth credentials by referring to the [Google OAuth Key + Secret guide](https://support.google.com/cloud/answer/6158849).

#### For Online Database Integration

If you're using an online database, ensure that you update the following variable in your `sample.env` file:

- `DATABASE_URL`: Replace this with your own database credentials. Obtain your Neon database URL by following the instructions provided in the [Connect with psql guide](https://neon.tech/docs/connect/query-with-psql-editor).

### Using the Setup Script (Recommended)

1. Clone this repository by running the following command in your terminal:

```
git clone https://github.com/Nantawat6510545543/KU-ACTIVE.git
```

2. Change your working directory to the project folder:

```
cd KU-ACTIVE
```

3. Execute the setup script based on your operating system:

   for **Mac/Linux**, use this command:
    ```
    chmod +x linux-setup-script.sh
    ./linux-setup-script.sh
    ```

   for **Windows**, use this command:
    ```
    window-setup-script.bat
    ```

Once the script completes, it will automatically run the server.

### Manual Installation

1. Clone this repository by running the following command in your terminal:

```
git clone https://github.com/Nantawat6510545543/ku-polls.git
```

2. Change your working directory to the project folder:

```
cd ku-polls
```

3. Create and activate a virtual environment:

   for **Mac/Linux**, use this command:
    ```
   python -m venv venv           # Create the virtual environment in "venv/" (only once)
   source ./venv/bin/activate           # Start the virtual environment in bash or zsh
    ```

   for **Windows**, use this command:
    ```
    python -m venv venv
    call  .\venv\Scripts\activate
    ```

4. Create a `.env` file by copying the contents of `sample.env`:

   for **Mac/Linux**, use this command:
    ```
   cp sample.env .env
   ```

   for **Windows**, use this command:
    ```
   copy sample.env .env
   ```

5. Install dependencies by running:

```
pip install -r requirements.txt
```

6. Create a new database by running migrations:

```
python manage.py migrate
```

7. Setup oauth system running setup_oauth:

```
python manage.py setup_oauth
```