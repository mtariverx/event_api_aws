from sqlalchemy.orm import relationship
from .base import Base

from sqlalchemy import Column, String, Integer, Float


class Client(Base):
    __tablename__ = 'client'

    pims_id = Column("pimsId", Integer, primary_key=True)
    first_name = Column("firstName", String(255))
    last_name = Column("lastName", String(255))
    balance = Column("balance", Float)

    classification_code = Column("classificationCode", String(255))
    classification_description = Column("classificationDescription", String(255))
    entered_date = Column("enteredDate", String(255)) #datetime YYYY-MM-DDTHH:MM:SS[.CC[C]]Z

    phone_numbers = relationship("PhoneNumber")
    pets = relationship("Patient")
    addresses = relationship("Address")
