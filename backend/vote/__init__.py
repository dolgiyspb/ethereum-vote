from flask import Flask

from flask_restful import Api
from web3 import Web3, HTTPProvider


app = Flask(__name__)
app.config.from_object('vote.config')
app.json_encoder = app.config['RESTFUL_JSON']['cls']

api_manager = Api(app)

web3 = Web3(HTTPProvider(app.config['NODE_ADDRESS']))

from vote import api
