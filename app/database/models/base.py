from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from app.database import Session

session = scoped_session(Session)
Base = declarative_base()
Base.query = session.query_property()
