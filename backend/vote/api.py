from flask_restful import Resource, reqparse
from http import HTTPStatus

from vote import api_manager
from vote.contract import create_vote_contract_manager

key_reqraser = reqparse.RequestParser()
key_reqraser.add_argument('key', required=True)

votes_reqparser = key_reqraser.copy()
votes_reqparser.add_argument('names', required=True, action='append')

vote_for_reqparser = key_reqraser.copy()
vote_for_reqparser.add_argument('candidate_index', type=int, required=True)


@api_manager.resource('/votes')
class Votes(Resource):
    def get(self):
        contracts = create_vote_contract_manager().load_all()
        return [{'address': c.address, 'candidates': c.candidates, 'closed': c.closed} for c in contracts]

    def post(self):
        data = votes_reqparser.parse_args()
        names = data['names']

        if len(names) != 2:
            raise NotImplementedError('Only votes with 2 candidates allowed')

        return (
            create_vote_contract_manager().deploy(args=names, key=data['key']),
            HTTPStatus.CREATED
        )


@api_manager.resource('/votes/<string:contract_address>')
class Vote(Resource):
    def get(self, contract_address):
        contract = create_vote_contract_manager().load(address=contract_address)
        return {
            'results': contract.results,
            'owner': contract.owner,
            'closed': contract.closed
        }

    def delete(self, contract_address):
        create_vote_contract_manager().load(address=contract_address).close(key=key_reqraser.parse_args()['key'])
        return '', HTTPStatus.NO_CONTENT


@api_manager.resource('/votes/<string:contract_address>/vote-for')
class VoteFor(Resource):
    def post(self, contract_address):
        args = vote_for_reqparser.parse_args()
        create_vote_contract_manager().load(address=contract_address).vote_for(
            candidate_index=args['candidate_index'], key=args['key']
        )