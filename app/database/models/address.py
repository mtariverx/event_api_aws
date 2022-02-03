from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, String, Integer

from .base import Base



class Address(Base):
    __tablename__ = 'address'

    id = Column('id', Integer, primary_key=True)

    address_line1 = Column("addressLine1", String(255))
    address_line2 = Column("addressLine2", String(255))
    city = Column("city", String(255))
    state_province = Column("stateProvince", String(255))
    postal_code = Column("postalCode", String(255))

    client_pims_id = Column(Integer, ForeignKey('client.pimsId'))

    patients = relationship("Patient")