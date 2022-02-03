from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from .base import Base

from sqlalchemy import Column, String, Integer


class MedicalNote(Base):
    __tablename__ = 'medicalNote'

    id = Column("id", Integer, primary_key=True)

    date_entered = Column("dateEntered", String(255))
    deleted = Column("deleted", Boolean)
    imported = Column("imported", String(255))

    note = Column("note", String(255))

    patient_id = Column(Integer, ForeignKey('patient.id'))

    status = Column("status", String(255))
    updated = Column("updated", String(255))
