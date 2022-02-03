from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

DIALECT = 'mysql'
DRIVER = 'pymysql'
USER = 'wes0459_woodb'
PASS = '.}Lid}Rea.IB'
HOST = 'shotvet-production-shotvet-production.aivencloud.com'
PORT = '10737'

engine = create_engine(f'mysql+pymysql://wesb0459_woodb:{PASS}@shotvet-production-shotvet-production.aivencloud.com:10737/evet')
Session = sessionmaker(bind=engine)

from app.database.models import *

Base.metadata.create_all(engine)
