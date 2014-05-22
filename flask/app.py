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
        print 'wat'
        print request.form['body']
        post_response = unirest.post(settings.API_URL + 'post/', headers={'Accept':'application/json'}, params={
            'body': request.form['body'],
            'user': '5377df73dae5f13c42854c4e'  # TODO: make this the logged in user
        })
        print post_response

        question_response = unirest.post(settings.API_URL + 'question/', headers={'Accept': 'application/json'}, params={
            'title': request.form['title'],
            'post': post_response.body['_id']
        })
        return redirect(url_for('question', qid=question_response.body['_id']))
    else:
        return render_template('question_ask.html', courses=json.dumps(courses))

@app.route('/question/<qid>')
def question(qid):
    url = settings.API_URL + 'question/' + qid
    response = unirest.get(url, headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})

    #get answers
    #answers = get_answers(qid)
    #pprint(answers)
    #response.body['answers'] = answers

    return render_template('question.html', data=response.body)

if __name__ == '__main__':
    app.run()

