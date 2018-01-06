from flask_restful import Resource, reqparse

from vote import api_manager
from vote.contract import deploy_vote_contract, create_vote_contract

votes_reqparser = reqparse.RequestParser()
votes_reqparser.add_argument('names', required=True, action='append')
votes_reqparser.add_argument('key', required=True)

vote_for_reqparser = reqparse.RequestParser()
vote_for_reqparser.add_argument('candidate_index', type=int, required=True)
vote_for_reqparser.add_argument('key', required=True)


@api_manager.resource('/votes')
class Votes(Resource):
    def post(self):
        data = votes_reqparser.parse_args()
        names = data['names']
        return deploy_vote_contract(names=names, key=data['key'])


@api_manager.resource('/votes/<string:contract_address>')
class Vote(Resource):
    def get(self, contract_address):
        return create_vote_contract(address=contract_address).results()


@api_manager.resource('/votes/<string:contract_address>/vote-for')
class VoteFor(Resource):
    def post(self, contract_address):
        args = vote_for_reqparser.parse_args()
        create_vote_contract(address=contract_address).vote_for(
            candidate_index=args['candidate_index'], key=args['key']
        )