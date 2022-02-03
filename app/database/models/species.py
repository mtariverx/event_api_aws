from sqlalchemy.orm import relationship
from .base import Base

from sqlalchemy import Column, String, Integer


class Species(Base):
    __tablename__ = 'species'

    id = Column("id", Integer, primary_key=True)
    description = Column("description", String(255))

    patients = relationship("Patient")