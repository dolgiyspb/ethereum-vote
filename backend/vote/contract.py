from vote import web3
from solc import compile_source
from contextlib import contextmanager


class ContractDeployer:
    def deploy(self, contract, args, key):
        acct = web3.eth.account.privateKeyToAccount(key)
        data = contract._encode_constructor_data(args=args)
        transaction = {
            'data': data,
            'gasPrice': web3.eth.gasPrice,
            'chainId': 1,
            'nonce': web3.eth.getTransactionCount(web3.eth.coinbase),
            'from': acct.address,
        }
        gas = web3.eth.estimateGas(transaction)
        transaction['gas'] = gas
        transaction['to'] = ''
        signed = acct.signTransaction(transaction)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        return {
            'address': tx_receipt['contractAddress'],
            'tx_hash': tx_hash,
        }


class VoteContractSource:
    def __init__(self, source_path):
        with open(source_path) as f:
            source_code = f.read()
        compiled_sol = compile_source(source_code)
        contract_interface = compiled_sol['<stdin>:Vote']
        self.contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

@contextmanager
def unlock_account(account, passphrase):
    web3.personal.unlockAccount(account , passphrase)
    yield
    web3.personal.lockAccount(account)

class VoteContractInstance:
    def __init__(self, address, contract):
        self.contract = contract
        self.address = address

    def candidates(self):
        return self.contract.call({'to': self.address}).Candidates()

    def results(self):
        first, second = self.contract.call({'to': self.address}).Candidates()
        for_first, for_second, against_all = self.contract.call({'to': self.address}).GetResults()
        make_vote_desc = lambda _name, _votes: {'name': _name, 'votes': _votes}
        return [
            make_vote_desc(name, votes) for name, votes in (
                (first, for_first), (second, for_second), ('against_all', against_all)
            )
        ]

    def vote_for(self, candidate_index, key):
        acct = web3.eth.account.privateKeyToAccount(key)
        tx = self.contract.buildTransaction({'to': self.address, 'from': acct.address}).VoteFor(candidate_index)
        signed = acct.signTransaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        return {
            'tx_hash': tx_hash,
        }

def create_vote_contract_source():
    return VoteContractSource(
        source_path='/contracts/Vote.sol'
    )

def create_vote_contract(address):
    return VoteContractInstance(
        address=address,
        contract=create_vote_contract_source().contract
    )

def deploy_vote_contract(names, key):
    if len(names) != 2:
        raise NotImplementedError('Only votes with 2 candidates allowed')

    return ContractDeployer().deploy(contract=create_vote_contract_source().contract, args=names, key=key)