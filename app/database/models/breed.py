from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import Column, String, Integer


class Breed(Base):
    __tablename__ = 'breed'

    id = Column("id", Integer, primary_key=True)
    description = Column("description", String(255))

    patients = relationship("Patient")

    def __repr__(self):
        return f"Breed <{self.id}> - description: {self.description}"