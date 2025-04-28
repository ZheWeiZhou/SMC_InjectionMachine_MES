from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

engine = create_engine("postgresql://postgres:postgres@140.135.106.49:5433/cax", echo=True)
Base = declarative_base()

class MachineHistory(Base):
    __tablename__ = 'MachineHistory'
    id = Column(Integer,primary_key=True)
    created_at = Column(DateTime(timezone = False), server_default=func.now())
    machine_name = Column(String)
    machine_status = Column(String)
    machine_feedback = Column(String)
    machine_curve = Column(String)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)