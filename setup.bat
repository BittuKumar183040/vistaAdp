@echo off
REM Creating and activating Virtual Environment
python -m venv venv
call .\venv\Scripts\activate

REM Logging pip version to a file
pip -V > pip_version.log

REM Display pip version in the console as well
type pip_version.log

REM Installing packages from requirements.txt (if it exists)
if exist requirements.txt (
	echo Installing dependencies from requirements.txt...
	pip install -r requirements.txt
) else (
	echo requirements.txt not found! Skipping package installation.
)

REM Installing Playwright
playwright install

REM Setting up Environment Variables
set /p USERID=Enter USERID (default:user_id): 
set /p PASSWORD=Enter PASSWORD (default:user_pass): 
(
	echo USERID=%USERID%
	echo PASSWORD=%PASSWORD%
) > .env

echo Setup complete :)
pause