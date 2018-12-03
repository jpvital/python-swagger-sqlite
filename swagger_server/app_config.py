import connexion, os
from swagger_server import encoder
from flask_sqlalchemy import SQLAlchemy
from .errors.errors import NotFoundException, DuplicateItemException, error_handler

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PATH_TO_DB = os.path.join(BASE_DIR, 'products.db')

APP = connexion.App(__name__, specification_dir='./swagger/', level='DEBUG')
APP.app.json_encoder = encoder.JSONEncoder
APP.add_api('swagger.yaml', arguments={'title': 'Factory product management'})
APP.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + PATH_TO_DB
APP.app.config['SQLALCHEMY_ECHO'] = True
APP.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.add_error_handler(NotFoundException, error_handler)
APP.add_error_handler(DuplicateItemException, error_handler)

