from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)


historyrouter = APIRouter()

db_url = "postgresql://postgres:postgres@140.135.106.49:5433/cax"
engine = create_engine(db_url)
Base = declarative_base()

Base = declarative_base()

class MachineHistory(Base):
    __tablename__ = 'MachineHistory'
    id = Column(Integer,primary_key=True)
    machine_name = Column(String)
    machine_setting = Column(String)
    machine_feedback = Column(String)
    machine_curve = Column(String)

class inserthistorydata_requestBody(BaseModel):
    machine_name:str
    machine_setting:str
    machine_feedback:str
    machine_curve:str

@historyrouter.post("/smc/injectionmachinemes/history/insertdata")
async def insertdata(requestData:inserthistorydata_requestBody):
    returnData       = {"status":"error"}
    machine_name     = requestData.machine_name
    machine_setting  = requestData.machine_setting
    machine_feedback = requestData.machine_feedback
    machine_curve    = requestData.machine_curve
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        insert_sql=MachineHistory.__table__.insert().values(
            machine_name=machine_name,
            machine_setting=machine_setting,
            machine_feedback=machine_feedback,
            machine_curve=machine_curve,
        )
        session.execute(insert_sql)
        session.commit()
        session.close()
        returnData = {"status": "success"}
    except:
        logging.error("Save machine data to db failed ...")
        pass
    return returnData






