from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import pika
import json
rabbitmq_account  = "cax"
rabbitmq_pass    = "cax521"
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)


commandrouter = APIRouter()

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

class machine_contorl_requestBody(BaseModel):
    machine_name:str
    target:str
    value:str

@commandrouter.post("/smc/injectionmachinemes/control")
async def insertdata(requestData:machine_contorl_requestBody):
    returnData       = {"status":"error"}
    machine_name     = requestData.machine_name
    target           = requestData.target
    value            = requestData.value
    
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='locallhost',
            credentials=pika.PlainCredentials(rabbitmq_account, rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=machine_name)
        commandbody = {"Target":target,"Value":value}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
                      routing_key=machine_name,
                      body=commandbody)
        connection.close()
        returnData = {"status": "success"}
    except:
        logging.error("Save machine data to db failed ...")
        pass
    return returnData






