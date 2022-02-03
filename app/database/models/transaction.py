from sqlalchemy.sql.schema import ForeignKey
from .base import Base

from sqlalchemy import Column, String, Integer, Float


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column('id', Integer, primary_key=True)
    amount = Column('amount', Float)
    invoice_number = Column('invoiceNumber', Integer)
    quantity = Column('quantity', Float)
    date_performed = Column('datePerformed', String(255))
    comments = Column('comments', String(255))
    description = Column('description', String(255))
    
    site_id = Column('siteId', Integer)
    pims_id = Column('sitePimsId', Integer)
    code_id = Column('codeId', Integer)

    client_pims_id = Column(Integer, ForeignKey('client.pimsId'))
    patient_pims_id = Column(Integer, ForeignKey('patient.id'))

