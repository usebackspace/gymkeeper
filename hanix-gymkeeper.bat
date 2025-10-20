@echo off
cd /d C:\gymkeeper
call env\Scripts\activate

:: Run Django server without opening a new window
start /b python manage.py runserver

timeout /t 5 >nul

start "" http://127.0.0.1:8000

pause
