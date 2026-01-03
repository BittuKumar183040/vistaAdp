@echo off
REM
python -m venv venv
call .\venv\Scripts\activate

REM
pip -V > pip_version.log

REM
type pip_version.log

REM
if exist requirements.txt (
	echo Installing dependencies from requirements.txt...
	pip install -r requirements.txt
) else (
	echo requirements.txt not found! Skipping package installation.
)

REM
playwright install

REM
set /p USERID=Enter USERID (default:user_id): 
set /p PASSWORD=Enter PASSWORD (default:user_pass): 
(
	echo USERID=%USERID%
	echo PASSWORD=%PASSWORD%
	echo LAT=%LAT%
	echo LON=%LON%
) > .env

echo Setup complete :)
pause