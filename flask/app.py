import os
import json
from pprint import pprint

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.assets import Environment, Bundle
import unirest

import settings

app = Flask(__name__)
app.debug = True

assets = Environment(app)
assets.load_path = [
    os.path.join(os.path.dirname(__file__), 'less'),
    os.path.join(os.path.dirname(__file__), 'js'),
    os.path.join(os.path.dirname(__file__), 'lib'),
]

css = Bundle('main.less', filters='less', output='gen/main.css', depends='bootstrap/less/*.less')
assets.register('css', css)

js = Bundle('jquery/jquery.js', 'jquery/jquery.optionTree.js', 'bootstrap/js/bootstrap.js', filters='rjsmin', output='gen/main.js')
assets.register('js', js)

#create add user helper function
def get_user(uid):
    response = unirest.get(settings.API_URL + 'user/' + uid, headers={'Content-Type':'application/json'})
    user = response.body
    return user

@app.route('/')
def home_page():
    response = unirest.get(settings.API_URL + 'question', headers={'Accept':'application/json'}, params={'embedded':'{"post":1}'})
    data = response.body['data']
    return render_template('home.html', data=data)

@app.route('/question/ask', methods=['GET', 'POST'])
def question_ask():
    courses = {
        'Computer Science': {
            '31': 'cs31',
            '131': 'cs131'
        }
    }
    if request.method == 'POST':
        param = {
            'body': request.form['body'],
            'title': request.form['title'],
            'user': '53797257945d32603d5196f9',
            'tags': request.form['tags'].split(),
        }
        response = unirest.post(settings.API_URL + 'question/', headers={'Accept':'application/json', 'Content-Type': 'application-json'}, params=json.dumps(param))

        return redirect(url_for('question', qid=response.body['id']))

    else:
        return render_template('question_ask.html', courses=json.dumps(courses))

@app.route('/question/<qid>')
def question(qid):
    url = settings.API_URL + 'question/' + qid
    response = unirest.get(url, headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})

    response.body['nAnswers'] = len(response.body['answer'])

    return render_template('question.html', data=response.body)

if __name__ == '__main__':
    app.run()

