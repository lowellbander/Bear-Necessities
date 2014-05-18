import json
from pprint import pprint

from flask import Flask, render_template, request
import unirest

import settings

app = Flask(__name__)
app.debug = True

@app.route('/')
def home_page():
    response = unirest.get(settings.API_URL + 'question', headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})
    return render_template('home.html', data=response.body)

@app.route('/question')
def question():
    qid = request.args['id']
    url = settings.API_URL + 'question/' + qid
    response = unirest.get(url, headers={'Content-Type':'application/json'}, params={'embedded':'{"post":1}'})

    post_url = settings.API_URL + 'post/' + response.body['post']['_id']
    post = unirest.get(post_url, headers={'Content-Type':'application/json'}, params={'embedded':'{"user":1}'})
    pprint(post.body)
    
    response.body['user'] = post.body['user']
    pprint(response.body)

    return render_template('question.html', data=response.body)

if __name__ == '__main__':
    app.run()

