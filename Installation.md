## Install instructions

### Using the Setup Script (Recommended)

1. Clone this repository by running the following command in your terminal:

```
git clone https://github.com/Nantawat6510545543/KU-ACTIVE.git
```

2. Change your working directory to the project folder:

```
cd KU-ACTIVE
```

3. Update the `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_SECRET_KEY`
   values in the [sample.env](sample.env)  file with your own credentials. You
   can obtain your Google OAuth Key and Secret by following the instructions
   provided in
   the [Google OAuth Key + Secret](https://support.google.com/cloud/answer/6158849).


4. Execute the setup script based on your operating system:

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

8.Import data using the "loaddata" command:

```
python manage.py loaddata data/polls.json data/users.json
```

9.(Optional) Load vote data to visualize a sample graph:

```
python manage.py loaddata data/vote.json
```