from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .base import Base

from sqlalchemy import Column, String, Integer, Float


class Patient(Base):
    __tablename__ = 'patient'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(255))
    color = Column("color", String(255))
    current_weight = Column("currentWeight", Float)
    date_of_birth = Column("dateOfBirth", String(255)) #datetime YYYY-MM-DDTHH:MM:SS[.CC]Z
    date_of_death = Column("dateOfDeath", String(255)) #datetime YYYY-MM-DDTHH:MM:SS[.CC]Z

    gender_description = Column("genderDescription", String(255))
    microchip = Column("microChip", String(255))
    rabies = Column("rabies", String(255))
    allergies = Column("allergies", String(255))
    alerts = Column("alerts", String(255))
    entered_date = Column("enteredDate", String(255))

    patient_breed = Column(Integer, ForeignKey('breed.id'))
    patient_species = Column(Integer, ForeignKey('species.id'))

    owner_pims_id = Column(Integer, ForeignKey('client.pimsId'))
    address_id = Column(Integer, ForeignKey('address.id'))
    
    transactions = relationship("Transaction")
