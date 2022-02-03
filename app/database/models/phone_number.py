from .base import Base

from sqlalchemy import ForeignKey, Column, String, Boolean, Integer, Float


class PhoneNumber(Base):
    __tablename__ = 'phoneNumber'
    
    id = Column('id', Integer, primary_key=True)
    number = Column('number', String(255))
    is_sms_enabled = Column('isSMSEnabled', Boolean)
    is_primary = Column('isPrimary', Boolean)

    client_pims_id = Column(Integer, ForeignKey('client.pimsId'))