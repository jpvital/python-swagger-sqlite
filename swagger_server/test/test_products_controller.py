# coding: utf-8

from __future__ import absolute_import
import os
from flask import json

from swagger_server.test import BaseTestCase

from ..app_config import BASE_DIR
MOCKS_DIR = os.path.join(BASE_DIR, 'test/mocks')

with open(MOCKS_DIR + '/sample_food_products_post.json') as json_data:
    PAYLOAD = json.load(json_data)

class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_get_products_200(self):
        """Test case for get_products

        Finds products by factory
        """
        headers = [('X_API_KEY', 'X_API_KEY_example')]
        response = self.client.open(
            '/products-api/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_products_200(self):
        """Test case for post_products

        Add a new product to a factory's inventory.
        """

        body = PAYLOAD #[ProductCreate(p) for p in PAYLOAD]

        headers = [('X_API_KEY', 'food')]
        response = self.client.open(
            '/products-api/products',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_products_400(self):
        """Test case for post_products with an invalid PAYLOAD

        Add a new product to a factory's inventory.
        """

        body = PAYLOAD[0] #[ProductCreate(p) for p in PAYLOAD]

        headers = [('X_API_KEY', 'X_API_KEY_example')]
        response = self.client.open(
            '/products-api/products',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_products_404(self):
        """Test case for post_products given a merchant name not in the DB

        Add a new product to a factory's inventory.
        """

        body = PAYLOAD #[ProductCreate(p) for p in PAYLOAD]

        headers = [('X_API_KEY', 'X_API_KEY_example')]
        response = self.client.open(
            '/products-api/products',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_products_409(self):
        """Test case for post_products with a duplicate product name

        Add a new product to a factory's inventory.
        """

        body = [PAYLOAD[0], PAYLOAD[0]] #[ProductCreate(p) for p in PAYLOAD]

        headers = [('X_API_KEY', 'food')]
        response = self.client.open(
            '/products-api/products',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assertEqual(response.status, '409 CONFLICT')


if __name__ == '__main__':
    import unittest
    unittest.main()
