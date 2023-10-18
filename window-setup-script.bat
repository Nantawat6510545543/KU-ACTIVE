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

:: Create .env file
copy sample.env .env

:: Run migrations
%PYTHON_CMD% manage.py migrate

:: Run setup oauth
%PYTHON_CMD% manage.py setup_oauth

:: Load initial data
@REM %PYTHON_CMD% manage.py loaddata data/action.json

:: Run tests
%PYTHON_CMD% manage.py test

:: Start the server
echo Starting the server...
%PYTHON_CMD% manage.py runserver --insecure
