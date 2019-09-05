@echo off

echo Starting the Flask server...
set FLASK_ENV=development
set FLASK_APP=server.py
flask run