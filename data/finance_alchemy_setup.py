'''
SQLAlchemy Setup

Where the setup for sqlalchemy engine and base are
'''
# pylint: disable=unnecessary-pass, too-few-public-methods
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
engine = create_engine(
    'mysql+pymysql://jv456:CS490Group#1@490sakila.mysql.database.azure.com/financestub',
    pool_size=10, max_overflow=20, echo=True)

class Base(DeclarativeBase):
    '''Base class'''
    pass
