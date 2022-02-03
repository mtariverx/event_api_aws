from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .base import Base

from sqlalchemy import Column, String, Integer


class Vaccine(Base):
    __tablename__ = 'vaccine'

    id = Column("id", Integer, primary_key=True)
    expiration_date = Column('expirationDate', String(255))
    date_given = Column('dateGiven', String(255))
    tag = Column('tag', String(255))
    manufacturer = Column('manufacturer', String(255))
    vaccine_description = Column('vaccineDescription', String(255))
    description = Column('description', String(255))

    patinet_id = Column(Integer, ForeignKey('patient.id'))
    client_pims_id = Column(Integer, ForeignKey('client.pimsId'))

    patients = relationship("Patient")
    clients = relationship("Client")