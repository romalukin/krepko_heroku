import os
from sqlalchemy import Table, Column,DateTime, Integer, String, Float,LargeBinary, MetaData, ForeignKey, engine, create_engine,Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.sql import func


db_url=os.environ['DATABASE_URL']
engine=create_engine(db_url,encoding='UTF8')
Base = declarative_base()
metadata = MetaData()

class Products(Base):
    __tablename__='products'
    id = Column(Integer, primary_key=True)
    name = Column( String(100) )
    old_price = Column( Integer )
    sale = Column( Integer )
    price = Column( Integer )
    category = Column( String(100) )
    url = Column( String(300) )
    
    

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insert_product(name = '', old_price = 0, sale = 0, price = 0, category = '', url = '')->None:
    ''' Insert product '''
    session=Session()
    db_product =Products( name=name, category= category,url=url,price=price,sale=sale)
    session.add(db_product)
    session.commit()   
    session.close()

def select_product(name: str) -> dict:
    ''' Select product '''
    session=Session()
    if session.query(Products).filter(Products.name==name).scalar():
        db_product = session.query(Products).filter(Products.name==name).one()
        output= {
                'name': db_product.name, 
                'category': db_product.category,
                'url':db_product.url,
                'old_price':db_product.old_price,
                'price':db_product.price}   
        session.close()   
        return {'status':True,'output':output}
    else: return {'status':False,'output': ''}

def delete_products() -> None:
    ''' Delete products '''
    session=Session()
    products = session.query(Products).all()
    session.delete(products)
    session.commit()
    session.close