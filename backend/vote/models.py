from vote import db

class Contract(db.Model):
    address = db.Column(db.String(42), primary_key=True)


class VoteContractRepo:
    def all(self):
        return Contract.query.all()

    def get(self, address):
        return Contract.query.get(address)

    def create(self, address):
        c = Contract(address=address)
        db.session.add(c)
        db.session.commit()
        return c


def create_vote_contract_repo():
    return VoteContractRepo()