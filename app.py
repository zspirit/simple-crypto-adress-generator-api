from flask import jsonify
from flask_restx import Resource
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import doc
from bitcoinaddress import Wallet
from eth_account import Account
import secrets
from models import Cryptoaddress
from config import app, ns, db

docs = FlaskApiSpec(app)

def getBitcoinAdress():
    wallet = Wallet(testnet=True)
    return wallet.address.testnet.pubaddr1

def getEthereumAdress():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return acct.address

#  Restful way of creating APIs through Flask Restful

def retrievData(data):
    res = []
    for item in data:
        res.append(item.serialize())
    return res


@ns.route('/list')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='list Address.', tags=['GET', 'ADRESS', 'GENERATOR'])
    def get(self, ):
        address = ""
        try:
            address = Cryptoaddress.query.all()
            res = retrievData(address)

            return {'status': 'Success',
                    'code': 200,
                    'address': res}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})

@ns.route('/list/<int:id>')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='Retrieve Address.', tags=['GET', 'ADRESS', 'GENERATOR'])
    def get(self, id, ):
        address = ''
        try:
            address = Cryptoaddress.query.get(id)
            res = address.serialize() if address else "Unable to find object with this ID : " + str(id)

            return {'status': 'Success',
                    'code': 200,
                    'address': res}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})

@ns.route('/<string:crypto>')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='Generate Address.', tags=['POST', 'ADRESS', 'GENERATOR'])
    def post(self, crypto,):
        address = ''
        try:
            match crypto.upper():
                case 'BTC':
                    address = getBitcoinAdress()
                case 'ETH':
                    address = getEthereumAdress()
                case default:
                    address = "Unsupported cryoto"

            if address != "Unsupported cryoto":
                new_entry = Cryptoaddress(address=address, crypto=crypto.upper(), private_key="")
                db.session.add(new_entry)
                db.session.commit()

            return {'status': 'Success',
                    'code': 200,
                    'crypto':crypto.upper(),
                    'address': address}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

