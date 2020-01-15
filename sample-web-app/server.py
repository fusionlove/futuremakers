# First we import the libraries we will need

import os
import pdb
import pyowm
from flask import Flask, render_template, session, request
from s3 import *
from config import *
from rekognition import *
from pdb import set_trace

# Then we make a new Flask app object
# and set up two secret keys, one for our app
# and one for the weather API

import passwords
bucket_name = passwords.bucket_name
s3_region = passwords.s3_region

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
owm = pyowm.OWM('2703e0179496b925772a76f52d131b19')


# Now we have our routes, which instruct the app what to do
# when particular web pages, such as /test, are visited.

# This is the route for the main page, localhost:5000

@app.route('/')
def hello_world():
    return render_template('index.html')


# To visit one of these pages, just enter its URL in the address bar
# after localhost:5000/

@app.route('/test')
def test_function():
    return render_template('test_template.html')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['name']
    return render_template('logout.html')

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/new')
def newpage():
    return render_template('new.html')


@app.route('/age_form')
def age_form():
    return render_template('age_form.html')

@app.route('/set_name', methods=['GET', 'POST'])
def set_name():
    name = request.form['name']
    session['name'] = name
    return render_template('index.html')

@app.route('/weather')
def weather():
    place = 'Atlanta, Georgia'
    observation = owm.weather_at_place(place)
    weather = observation.get_weather()
    return render_template('weather.html', weather=weather, place=place)

@app.route('/start')
def start():
    observation = owm.weather_at_place('London,GB')
    w = observation.get_weather()
    return render_template('start.html', w=w)


# This route listens for a POST request containing a file
# to upload. The POST request is sent by the browser when the user uploads
# a file.

@app.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files["user_file"]

        # These attributes are also available

        # file.filename               # The actual name of the file
        # file.content_type
        # file.content_length
        # file.mimetype


    url = "https://" + bucket_name + '.s3.' + s3_region + '.amazonaws.com/' + file.filename
    print(url)
    output = upload_file_to_s3(file, bucket_name)

    labels = detect_labels(bucket_name, file.filename)

    return render_template('show_image.html', url = url,
      labels=labels)


# This piece of code starts the app.
# It has to be at the end because nothing after it will run
# as the app goes into a listening loop

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)