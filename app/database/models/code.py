from .base import Base

from sqlalchemy import Column, String, Integer


class Code(Base):
    __tablename__ = 'code'

    id = Column("id", Integer, primary_key=True)

    code = Column("code", String(255))
    item_description = Column("itemDescription", String(255))
    code_category = Column("codeCategory", Integer)
    code_category_description = Column("codeCategoryDescription", String(255))
