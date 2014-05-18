import os
import json

from flask import Flask, render_template, send_from_directory
from flask.ext.assets import Environment, Bundle
import unirest

import settings

app = Flask(__name__)
app.debug = True

assets = Environment(app)
assets.load_path = [
    os.path.join(os.path.dirname(__file__), 'less'),
    os.path.join(os.path.dirname(__file__), 'js'),
    os.path.join(os.path.dirname(__file__), 'bower_components'),
]

css = Bundle('main.less', filters='less', output='gen/main.css', depends='bootstrap/less/*.less')
assets.register('css', css)

js = Bundle('jquery/dist/jquery.js', 'bootstrap/dist/js/bootstrap.js', filters='rjsmin', output='gen/main.js')
assets.register('js', js)

@app.route('/')
def home_page():
    response = unirest.get(settings.API_URL + 'question', headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})
    return render_template('home.html', data=response.body)

if __name__ == '__main__':
    app.run()

