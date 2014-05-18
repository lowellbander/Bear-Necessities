import datetime
API_URL = "https://qa-dev.uclalibrary.org/"

#SERVER_NAME = '0.0.0.0'
#SERVER_NAME = '127.0.0.1:8726'

post_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'body': {
        'type': 'string',
        'default': 'This post has no body.',
    },
    'upvotes': {
        'type': 'integer',
        'default': 0,
    },
    'downvotes': {
        'type': 'integer',
        'default': 0,
    },
    'views': {
        'type': 'integer',
        'default': 0,
    },
    'active': {
        'type': 'bool',
        'default': True,
    },
    'user': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'user',
            'field': '_id',
            'embeddable': True,
        },
    },
}

question_schema = {
    'title': {
        'type': 'string',
        'default': 'This question has no title.',
    },
    'post': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'post',
            'field': '_id',
            'embeddable': True,
        },
    },
    'tags': {
        'type': 'list',
    },
    'courses': {
        'type': 'list',
    },
}

answer_schema = {
    'post': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'post',
            'field': '_id',
            'embeddable': True,
        },
    },
    'question': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'question',
            'field': '_id',
            'embeddable': True,
        },
    },
}

comment_schema = {
    'post': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'post',
            'field': '_id',
            'embeddable': True,
        },
    },
    'parent': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'post',
            'field': '_id',
            'embeddable': True,
        },
    },
}

answer_schema = {
    'post': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'post',
            'field': '_id',
            'embeddable': True,
        },
    },
    'question': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'question',
            'field': '_id',
            'embeddable': True,
        },
    },
}

user_schema = {
    'name': {
        'type': 'string',
        'default': 'NO NAME',
    },
    'major': {
        'type': 'list',
    },
    'minor': {
        'type': 'list',
    },
    'reputation': {
        'type': 'int',
        'default': 0,
    },
    'member_since': {
        # possibly redundant to implicit, automatic '_created'
        'type': 'datetime',
    },
}

post = {
    'schema': post_schema,
}

question = {
    'schema': question_schema,
}

answer = {
    'schema': answer_schema,
}

comment = {
    'schema': comment_schema,
}

user = {
    'schema': user_schema,
}

DOMAIN = {
    'post': post,
    'question': question,
    'answer': answer,
    'user': user,
}
# Let's just use the local mongod instance. Edit as needed.

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#following two lines caused problems. Not sure if will be necessary eventually
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'
MONGO_DBNAME = 'beardb'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
