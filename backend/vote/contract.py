from solc import compile_source

from vote.models import create_vote_contract_repo
from vote import web3, app


class VoteContractManager:
    def __init__(self, contract_definition):
        self.contract_definition = contract_definition

    def deploy(self, args, key):
        acct = web3.eth.account.privateKeyToAccount(key)
        data = self.contract_definition._encode_constructor_data(args=args)
        transaction = {
            'data': data,
            'gasPrice': web3.eth.gasPrice,
            'chainId': web3.net.version,
            'nonce': web3.eth.getTransactionCount(acct.address),
            'from': acct.address,
        }
        gas = web3.eth.estimateGas(transaction)
        transaction['gas'] = gas
        transaction['to'] = ''
        signed = acct.signTransaction(transaction)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        address = tx_receipt['contractAddress']
        create_vote_contract_repo().create(address)
        return {
            'address': address,
            'tx_hash': tx_hash,
        }

    def load_all(self):
        return [
            VoteContract(address=contract.address, contract_definition=self.contract_definition)
            for contract in create_vote_contract_repo().all()
        ]

    def load(self, address):
        db_model = create_vote_contract_repo().get(address=address)
        return VoteContract(address=db_model.address, contract_definition=self.contract_definition)

class VoteContract:

    def __init__(self, address, contract_definition):
        self.contract_definition = contract_definition
        self.address = address

    @property
    def candidates(self):
        return self._call('Candidates')

    @property
    def results(self):
        first, second = self.candidates
        for_first, for_second, against_all = self._call('GetResults')
        make_vote_desc = lambda _name, _votes: {'name': _name, 'votes': _votes}
        return [
            make_vote_desc(name, votes) for name, votes in (
                (first, for_first), (second, for_second), ('against_all', against_all)
            )
        ]

    @property
    def closed(self):
        return self._call('closed')

    @property
    def owner(self):
        return self._call('owner')

    def vote_for(self, candidate_index, key):
        return self._signed_call('VoteFor', key, candidate_index)

    def close(self, key):
        return self._signed_call('Close', key)

    def _signed_call(self, method_name, key, *args):
        acct = web3.eth.account.privateKeyToAccount(key)
        method = getattr(self.contract_definition.buildTransaction({'to': self.address, 'from': acct.address}), method_name)
        tx = method(*args)
        tx['nonce'] = web3.eth.getTransactionCount(acct.address)
        signed = acct.signTransaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        return {
            'tx_hash': tx_hash,
        }

    def _call(self, method_name, *args):
        method = getattr(self.contract_definition.call({'to': self.address}), method_name)
        return method(*args)

def create_vote_contract_definition():
    with open(app.config['VOTE_CONTRACT_SOURCE_PATH']) as f:
        source_code = f.read()
    compiled_sol = compile_source(source_code)
    contract_interface = compiled_sol['<stdin>:Vote']
    return web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])


def create_vote_contract_manager():
    return VoteContractManager(create_vote_contract_definition())
