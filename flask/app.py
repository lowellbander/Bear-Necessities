import os
import json
from pprint import pprint

from flask import Flask, render_template, request
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

js = Bundle('jquery/dist/jquery.js', 'bootstrap/dist/js/bootstrap.js', filters='rjsmin', output='gen/main.js')
assets.register('js', js)

#create add user helper function
def get_user(uid):
    response = unirest.get(settings.API_URL + 'user/' + uid, headers={'Content-Type':'application/json'})
    user = response.body
    return user

def get_answers(qid):
    #qid == question._id

    #get all questions
    response = unirest.get(settings.API_URL + 'answer/', headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})
    answers = response.body['_items']

    #filter for the ones that have qid has their question's id
    relevant = []
    for answer in answers:
        if answer['question'] == qid:
            answer['post']['user'] = get_user(answer['post']['user'])
            relevant.append(answer)
    return relevant

@app.route('/test')
def test():
    _id = request.args['id']
    get_answers(_id)
    #get_user(_id)
    return "testing..."

@app.route('/')
def home_page():
    response = unirest.get(settings.API_URL + 'question', headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})
    return render_template('home.html', data=response.body)

@app.route('/question/<qid>')
def question(qid):
    url = settings.API_URL + 'question/' + qid
    response = unirest.get(url, headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})

    #get the post (parent)
    post_url = settings.API_URL + 'post/' + response.body['post']['_id']
    post = unirest.get(post_url, headers={'Content-Type':'application/json'}, params={'embedded':'{"user":1}'})
    print post.code
    
    response.body['post']['user'] = post.body['user'] if post.code == 200 else {}

    response.body['votes'] = response.body['post']['upvotes'] - response.body['post']['downvotes'] 
    #pprint(response.body)

    #get answers
    answers = get_answers(qid)
    pprint(answers)
    response.body['answers'] = answers

    return render_template('question.html', data=response.body)

if __name__ == '__main__':
    app.run()

