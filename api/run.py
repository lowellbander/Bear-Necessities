import os

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods

app = Flask(__name__)
app.debug = True

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'jungle_book',
)

db = MongoEngine(app)
api = MongoRest(app)

class User(db.Document):
    name = db.StringField(default='NO NAME')
    major = db.ListField(db.StringField())
    minor = db.ListField(db.StringField())
    reputation = db.IntField(default=0)

class Post(db.Document):
    body = db.StringField(default='This post has no body.')
    upvotes = db.IntField(default=0)
    downvotes = db.IntField(default=0)
    views = db.IntField(default=0)
    active = db.BooleanField(default=True)
    user = db.ReferenceField(User)
    meta = {'allow_inheritance': True}

class Comment(Post):
    parent = db.ReferenceField(Post)

class Question(Post):
    title = db.StringField(default='This question has no title.')
    tags = db.ListField(db.StringField())
    course = db.StringField()
    major = db.StringField()

class Answer(Post):
    question = db.ReferenceField(Question)

class UserResource(Resource):
    document = User
    filters = {
        'name': [ops.Exact, ops.Contains]
    }

class AnswerResource(Resource):
    document = Answer
    filters = {
        'question': [ops.Exact]
    }

class CommentResource(Resource):
    document = Comment
    filters = {
        'parent': [ops.Exact]
    }

class QuestionResource(Resource):
    document = Question
    related_resources = {
        'user': UserResource,
        'answer': AnswerResource
    }
    filters = {
        'tag': [ops.Exact, ops.Contains],
        'course': [ops.Exact, ops.Contains],
        'major': [ops.Exact, ops.Contains],
    }

@api.register(name='user', url='/user/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='question', url='/question/')
class QuestionView(ResourceView):
    resource = QuestionResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='answer', url='/answer/')
class AnswerView(ResourceView):
    resource = AnswerResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='comment', url='/comment/')
class CommentView(ResourceView):
    resource = CommentResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

if __name__ == '__main__':
    #app.run()
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

