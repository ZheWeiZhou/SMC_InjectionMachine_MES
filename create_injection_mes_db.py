from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import bcrypt 
engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/cax", echo=True)
Base = declarative_base()

class MachineHistory(Base):
    __tablename__    = 'MachineHistory'
    id               = Column(Integer,primary_key=True)
    created_at       = Column(DateTime(timezone = False), server_default=func.now())
    machine_name     = Column(String)
    machine_status   = Column(String)
    machine_feedback = Column(String)
    machine_curve    = Column(String)

class UserConfig(Base):
    __tablename__ = 'UserConfig'
    id            = Column(Integer,primary_key=True)
    created_at    = Column(DateTime(timezone = False), server_default=func.now())
    username      = Column(String)
    useraccount   = Column(String)
    userpassword  = Column(String)
    token         = Column(String)

class Machinelist(Base):
    __tablename__ = 'Machinelist'
    id              = Column(Integer,primary_key=True)
    created_at      = Column(DateTime(timezone = False), server_default=func.now())
    machinename     = Column(String)
    activate        = Column(String)
    troubleshooting = Column(String)

class BayesianNetworkTrainData(Base):
    __tablename__ = 'BayesianNetworkTrainData'
    id               = Column(Integer,primary_key=True)
    machinehistoryid = Column(Integer)
    created_at       = Column(DateTime(timezone = False), server_default=func.now())
    machine_name     = Column(String)
    model_result     = Column(String) 
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create Admin user
Session = sessionmaker(bind=engine)
session = Session()

admintoken  = "8d6d4e85-b277-4102-8ffd-defcc7b7b9f9" # uuid.uuid4()
username    = "admin"
useraccount = "admin"

userpassword = "admin"
hashed_password = bcrypt.hashpw(userpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
insert_sql = UserConfig.__table__.insert().values(
                    username     = username,
                    useraccount  = useraccount,
                    userpassword = hashed_password,
                    token        = admintoken
                )

session.execute(insert_sql)
session.commit()
session.close()
