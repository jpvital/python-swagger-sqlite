import sqlalchemy

from .db_config import (
    Product,
    ProductMaterial,
    ProductProperty,
    ProductPropertyGroup,
    ProductPropertyGroupElement
)
from ..shared import DB
from ..errors.errors import NotFoundException, DuplicateItemException

# # Get the top-level logger object
# log = logging.getLogger()

# # make it print to the console.
# console = logging.StreamHandler()
# log.addHandler(console)

def json_2_db(payload: [dict]) -> [Product]:
    """Convert the incoming payload into a format accepted by the database"""
    products = []
    for _p in payload:
        new_product = Product(name=_p['name'], manufacturer=_p['manufacturer'])
        del _p['name']
        del _p['manufacturer']

        #bill of materials
        if 'billOfMaterials' in _p.keys():
            for _m in _p['billOfMaterials'].keys():
                new_material = ProductMaterial(
                    name=_m,
                    quantity=_p['billOfMaterials'][_m]['quantity'],
                    units=_p['billOfMaterials'][_m]['units']
                )
                new_product.bill_of_materials.append(new_material)
            del _p['billOfMaterials']

        for k in _p.keys():
            #product property group
            if isinstance(_p[k], list):
                new_property_group = ProductPropertyGroup(name=k)
                #product property group elements
                for elem in _p[k]:
                    new_property_group.elements.append(ProductPropertyGroupElement(name=elem))
                new_product.product_property_groups.append(new_property_group)
            #product property
            else:
                new_property = ProductProperty(name=k, value=_p[k])
                new_product.product_properties.append(new_property)
        products.append(new_product)
    return products

def db_2_json(products: [Product]) -> [dict]:
    """Convert the result of a database query into a dictionary
    to be returned to the user in JSON format"""
    parsed_products = []
    for unparsed_item in products:
        new_product = {}
        new_product['id'] = unparsed_item.id
        new_product['name'] = unparsed_item.name
        #product properties
        for prop in unparsed_item.product_properties:
            new_product[prop.name] = prop.value

        #product materials
        new_product['billOfMaterials'] = {}
        for mat in unparsed_item.bill_of_materials:
            new_product['billOfMaterials'][mat.name] = {}
            new_product['billOfMaterials'][mat.name]['quantity'] = mat.quantity
            new_product['billOfMaterials'][mat.name]['units'] = mat.units

        #product property groups
        for group in unparsed_item.product_property_groups:
            elements = [e.name for e in group.elements]
            new_product[group.name] = elements
        #print(new_product)
        parsed_products.append(new_product)
    return parsed_products

def insert_products(manufacturer: str, products: [dict]) -> None:
    """Save a list of new products into the database"""
    for unparsed_item in products:
        unparsed_item['manufacturer'] = manufacturer

    parsed_products = json_2_db(products)
    for _p in parsed_products:
        _p.manufacturer = manufacturer
        DB.session.add(_p)
    try:
        DB.session.commit()
    except sqlalchemy.exc.IntegrityError as _e:
        if 'FOREIGN' in str(_e):
            raise NotFoundException(message='Could not find manufacturer.')
        elif 'UNIQUE' in str(_e):
            raise DuplicateItemException(message='Product name must be unique per manufacturer')

def select_products(manufacturer):
    """Retrieve a manufacturers products"""
    products = DB.session.query(Product).filter_by(manufacturer=manufacturer)
    return db_2_json(products)
