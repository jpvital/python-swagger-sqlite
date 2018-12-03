from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..shared import DB
BASE_MODEL = DB.Model

class Manufacturer(BASE_MODEL):
    #name
    #industry
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
    #product_id
    #name
    #quantity
    #units
    __tablename__ = 'productMaterial'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    quantity = Column(String(50), nullable=False)
    units = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class ProductProperty(BASE_MODEL):
    #product_id
    #name
    #value
    __tablename__ = 'productProperty'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    value = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class ProductPropertyGroup(BASE_MODEL):
    #product_id
    #name
    #type
    __tablename__ = 'productPropertyGroup'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(50), nullable=False)
    elements = relationship('ProductPropertyGroupElement', cascade='all, delete-orphan')


    def __repr__(self):
        return self.name

class ProductPropertyGroupElement(BASE_MODEL):
    #product_property_group_id
    #name
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

manufacturer_default_data = [
    Manufacturer(name='textile', industry='textile'),
    Manufacturer(name='food', industry='food')
]

def create_database():
    DB.drop_all()
    DB.create_all()
    for m in manufacturer_default_data:
        DB.session.add(m)
    DB.session.commit()