from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

app = Flask(__name__)  # Flask app instance initiated
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo_crypto_addr.db'
db = SQLAlchemy(app)

api = Api(app,
          version='1.0',
          title='Simple Crypto Adress Generator API',
          description='This is a simple demo for a Crypto Adress Generator API ')  # Flask restful wraps Flask app around it.

ns = api.namespace('/', description='Demo : Crypto Adress Generator API')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Simple Crypto Adress Generator API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})