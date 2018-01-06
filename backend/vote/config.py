NODE_ADDRESS = 'http://node:8545'
DEBUG = True

from vote import json

RESTFUL_JSON = {
    'cls': json.CustomJSONEncoder
}

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@db/postgres'