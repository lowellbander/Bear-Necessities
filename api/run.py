from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods  

app = Flask(__name__)

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'jungle_book',
)

db = MongoEngine(app)
api = MongoRest(app)

class Post(db.Document):
    body = db.StringField(default='This post has no body.')
    upvotes = db.IntField(default=0)
    downvotes = db.IntField(default=0)
    views = db.IntField(default=0)
    active = db.BooleanField(default=True)
    user = db.EmbeddedDocumentField(User)

class User(db.EmbeddedDocument):
    name = db.StringField(default='NO NAME')
    major = db.ListField(db.StringField())
    minor = db.ListField(db.StringField())
    reputation = db.IntField(default=0)

class Question(Post):
    title = db.StringField(default='This question has no title.')
    tags = db.ListField(db.StringField())
    course = db.StringField()
    major = db.StringField()

class Answer(Post):
    question = db.ReferenceField(Question)

class Comment(Post):
    parent = db.ReferenceField(Comment)


class QuestionResource(Resource):
    document = Question
    filters = {
        'tag': [ops.Exact, ops.Icontains],
        'course': [ops.Exact, ops.Icontains],
        'major': [ops.Exact, ops.Icontains],
    }

@api.register(name='question', url='/question/')
class QuestionView(ResourceView):
    resource = QuestionResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]
    