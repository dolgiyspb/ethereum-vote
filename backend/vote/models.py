from vote import db

class Contract(db.Model):
    address = db.Column(db.String(42), primary_key=True)