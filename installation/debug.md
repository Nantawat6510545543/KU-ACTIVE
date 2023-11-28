## Debug Installation Guide

To enable debugging for the application, follow these steps:

1) Set the `DEBUG` variable in the `sample.env` file to True.
2) Install debug dependencies by running the following command:
    ```
    pip install -r installation/debug_requirements.txt
    ```

3) If you decide to switch `DEBUG` to `False` and make changes to static files, execute the following command after updating the `DEBUG` variable:
    ```
    python manage.py collectstatic
    ```