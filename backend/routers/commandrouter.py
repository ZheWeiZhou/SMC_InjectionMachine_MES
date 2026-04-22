from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import pika
import json
from typing import List
rabbitmq_account  = "cax"
rabbitmq_pass    = "cax521"
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)


commandrouter = APIRouter()

with open('config.json', 'r', encoding='utf-8') as f:
    envparameter = json.load(f)
    
engine = create_engine(envparameter["db_url"])
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
            host='rabbitmq',
            credentials=pika.PlainCredentials(rabbitmq_account, rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=machine_name)
        
        commandbody = {"Target":target,"Value":value}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
                      routing_key=machine_name,
                      body=commandbody,
                    #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                      )
        connection.close()
        returnData = {"status": "success"}
    except Exception as e:
        print(e)
        logging.error("Save machine data to db failed ...")
        pass
    return returnData

class TargetValueItem(BaseModel):
    target: str
    value: str
class machine_multicontorl_requestBody(BaseModel):
    machine_name:str
    command:List[TargetValueItem]
    machine_Protocol :str = "euromap77"

@commandrouter.post("/smc/injectionmachinemes/multicontrol")
async def insertdata(requestData:machine_multicontorl_requestBody):
    returnData       = {"status":"error"}
    machine_name     = requestData.machine_name
    command          = requestData.command
    machine_Protocol = requestData.machine_Protocol
    try:
        match machine_Protocol:
            case "euromap77":
                for commanditem in command:
                    target = commanditem.target
                    value  = commanditem.value
                    float(value)
                    connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host='rabbitmq',
                        credentials=pika.PlainCredentials(rabbitmq_account, rabbitmq_pass)
                    ))
                    channel = connection.channel()
                    channel.queue_declare(queue=machine_name)
                    
                    commandbody = {"Target":target,"Value":value}
                    commandbody = json.dumps(commandbody)
                    channel.basic_publish(exchange='',
                                routing_key=machine_name,
                                body=commandbody,
                                #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                                )
                    connection.close()
                returnData = {"status": "success"}
            case "euromap63":
                batchtarget = []
                batchvalue  = []
                for commanditem in command:
                    target = commanditem.target
                    value  = commanditem.value
                    float(value)
                    batchtarget.append(target)
                    batchvalue.append(value)
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host='rabbitmq',
                        credentials=pika.PlainCredentials(rabbitmq_account, rabbitmq_pass)
                    ))
                commandbody = {"Target":batchtarget,"Value":batchvalue,"Batch":1}
                commandbody = json.dumps(commandbody)
                channel = connection.channel()
                channel.queue_declare(queue=machine_name)
                channel.basic_publish(
                    exchange='',
                    routing_key=machine_name,
                    body=commandbody,
                #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                )
                returnData = {"status": "success"}
            case _:
                returnData = {"status": "error","message":"unknown machine protocol"}
    except Exception as e:
        print("ERROR @@@@@@@@@@@@@",e)
        logging.error(e)
        pass
    return returnData



