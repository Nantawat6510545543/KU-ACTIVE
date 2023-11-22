## Manual Installation

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