from flask import jsonify
from flask_restx import Resource
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import doc
from bitcoinaddress import Wallet
from eth_account import Account
import secrets
from models import Cryptoaddress
from config import app, db, api

docs = FlaskApiSpec(app)

def getBitcoinAdress():
    wallet = Wallet(testnet=True)
    return wallet.address.testnet.pubaddr1, wallet.key.testnet.wif

def getEthereumAdress():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return acct.address, private_key

#  Restful way of creating APIs through Flask Restful

def retrievData(data):
    res = []
    for item in data:
        res.append(item.serialize())
    return res


@api.route('/list')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='list Address.', tags=['GET', 'ADDRESS', 'GENERATOR'])
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

@api.route('/list/<int:id>')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='Retrieve Address.', tags=['GET', 'ADDRESS', 'GENERATOR'])
    def get(self, id, ):
        address = ''
        try:
            address = Cryptoaddress.query.get_or_404(id)
            res = address.serialize()

            return {'status': 'Success',
                    'code': 200,
                    'address': res}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})

@api.route('/delete/<int:id>')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='Delete Address.', tags=['DELETE', 'ADDRESS', 'GENERATOR'])
    def delete(self, id, ):
        address = Cryptoaddress.query.get_or_404(id)
        res = "Address " + str(id) + " was successfully deleted"
        try:
            db.session.delete(address)
            db.session.commit()
            return {'status': 'Success',
                    'code': 200,
                    'address': res}
        except:
            return 'There was an issue deleting  address'

@api.route('/<string:crypto>')
class CryptoAdressGeneratorAPI(MethodResource, Resource):
    @doc(description='Generate Address.', tags=['POST', 'ADDRESS', 'GENERATOR'])
    def post(self, crypto,):
        address = ''
        pkey = ''
        try:
            match crypto.upper():
                case 'BTC':
                    address, pkey = getBitcoinAdress()
                case 'ETH':
                    address, pkey = getEthereumAdress()
                case default:
                    address = "Unsupported cryoto"

            if address != "Unsupported cryoto":
                new_entry = Cryptoaddress(address=address, crypto=crypto.upper(), private_key=pkey)
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

