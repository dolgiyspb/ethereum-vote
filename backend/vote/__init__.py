from flask import Flask
from flask.json import JSONEncoder
from flask_restful import Api
from web3 import Web3, HTTPProvider
from web3.utils.datastructures import HexBytes

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.config.setdefault('RESTFUL_JSON', {})['cls'] = app.json_encoder = CustomJSONEncoder
api_manager = Api(app)
web3 = Web3(HTTPProvider('http://node:8545'))

web3.personal.newAccount('1q2w3e')

from vote import api
