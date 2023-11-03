@echo off
echo Setting up the project environment...

:: Check if py is available, if not, check if python3 is available, if not, fall back to python
where py > nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py
) else (
    where python3 > nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=python3
    ) else (
        set PYTHON_CMD=python
    )
)

:: Create and activate virtual environment
%PYTHON_CMD% -m venv venv
call .\venv\Scripts\activate

:: Install requirements
pip install -r requirements.txt

:: Install Django Debug Toolbar if DEBUG is True in .env
findstr /R /C:"DEBUG = True" .\.env > nul || findstr /R /C:"DEBUG=True" .\.env > nul || findstr /R /C:"DEBUG =True" .\.env > nul

if %errorlevel%==0 (
    echo DEBUG is set to True. Installing Django Debug Toolbar...
    pip install django-debug-toolbar
) else (
    echo AAAAAAAAAAAAAAAAAAAAAAAAAAA
)

:: Create .env file
copy sample.env .env

:: Run migrations
%PYTHON_CMD% manage.py migrate

:: Run setup oauth
%PYTHON_CMD% manage.py setup_oauth

:: Run tests
%PYTHON_CMD% manage.py test

:: Start the server
echo Starting the server...
%PYTHON_CMD% manage.py runserver --insecure