import logging
from flask_testing import TestCase
from ..app_config import APP


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        return APP.app
