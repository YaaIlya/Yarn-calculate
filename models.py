from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Yarn(Base):
    __tablename__ = 'yarns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    color = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Yarn(brand={self.brand}, name={self.name}, country={self.country}, color={self.color}, quantity={self.quantity})>"
