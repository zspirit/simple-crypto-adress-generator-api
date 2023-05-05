from config import db
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Cryptoaddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), nullable=False) #crypto addr
    crypto = db.Column(db.String(250), nullable=False) #eth or btc
    private_key = db.Column(db.String(250), nullable=False)  # private_key
    #private_key = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Cryptoaddress %r' % self.id

    def serialize(self):
        return {"id": self.id,
                "address": self.address,
                "crypto": self.crypto,
                "private_key": self.private_key,
                "date_created": self.date_created,}

