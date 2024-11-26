from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Band(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    upload = Column(Float)
    download = Column(Float)
    date = Column(String)
    ping = Column(Float)
    error = Column(Boolean, default=True)

