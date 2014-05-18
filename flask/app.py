import json

from flask import Flask, render_template
import unirest

import settings

app = Flask(__name__)
app.debug = True

@app.route('/')
def home_page():
    response = unirest.get(settings.API_URL + 'question', headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})
    return render_template('home.html', data=response.body)

if __name__ == '__main__':
    app.run()