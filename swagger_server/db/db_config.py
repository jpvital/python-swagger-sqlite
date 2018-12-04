from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..shared import DB
BASE_MODEL = DB.Model

class Manufacturer(BASE_MODEL):
    __tablename__ = 'manufacturer'
    name = Column(String(50), unique=True, nullable=False, primary_key=True)
    industry = Column(String(50), nullable=False,)
    products = relationship('Product', cascade='all, delete-orphan')

    def __repr__(self):
        return self.name

class Product(BASE_MODEL):
    #manufacturer_id
    #name
    #type
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String, ForeignKey('manufacturer.name'), nullable=False)
    name = Column(String(50), nullable=False)
    product_properties = relationship('ProductProperty', cascade='all, delete-orphan')
    product_property_groups = relationship('ProductPropertyGroup', cascade='all, delete-orphan')
    bill_of_materials = relationship('ProductMaterial', cascade='all, delete-orphan')
    __table_args__ = (UniqueConstraint('manufacturer', 'name', name='uix_1'),)

    def __repr__(self):
        return self.name

class ProductMaterial(BASE_MODEL):
    """this table contains all the values seen in the billOfMaterials
    field in the JSON payloads"""

    __tablename__ = 'productMaterial'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    quantity = Column(String(50), nullable=False)
    units = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class ProductProperty(BASE_MODEL):
    """this table stores all the key-value pairs in the top
    level of the JSON payload"""

    __tablename__ = 'productProperty'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    value = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class ProductPropertyGroup(BASE_MODEL):
    """this table stores the names of the fields
    which contain lists of values in the JSON payload"""

    __tablename__ = 'productPropertyGroup'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    elements = relationship('ProductPropertyGroupElement', cascade='all, delete-orphan')


    def __repr__(self):
        return self.name

class ProductPropertyGroupElement(BASE_MODEL):
    """This table stores all the values inside those lists"""
    __tablename__ = 'propertyGroupElement'
    id = Column(Integer, primary_key=True)
    product_property_group_id = Column(
        Integer,
        ForeignKey('productPropertyGroup.id'),
        nullable=False
    )
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

MANUFACTURER_DEFAULT_DATA = [
    Manufacturer(name='textile', industry='textile'),
    Manufacturer(name='food', industry='food')
]

def create_database():
    DB.drop_all()
    DB.create_all()
    for _m in MANUFACTURER_DEFAULT_DATA:
        DB.session.add(_m)
    DB.session.commit()
    