import connexion
from flask import request

from src.models.product import Product  # noqa: E501
from ..db.helpers import insert_products, select_products


def get_products():  # noqa: E501
    """Finds products by factory

     # noqa: E501

    :param X_API_KEY: Name of the manufacturer (eg &#39;textils&#39;, &#39;food&#39;)
    :type X_API_KEY: str

    :rtype: List[Product]
    """
    manufacturer_name = request.headers.get('X_API_KEY')
    return select_products(manufacturer_name)


def post_products(body):  # noqa: E501
    """Add a new product to a factory&#39;s inventory.

     # noqa: E501

    :param X_API_KEY: Name of the manufacturer (eg &#39;textils&#39;, &#39;food&#39;)
    :type X_API_KEY: str
    :param body: List of product objects to be added to the inventory.
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [Product.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
        manufacturer_name = request.headers.get('X_API_KEY')
        insert_products(manufacturer_name, body)
