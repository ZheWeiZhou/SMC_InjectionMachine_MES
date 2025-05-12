from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime,text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import redis
from datetime import datetime
import json
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)

red = redis.Redis(host='Redis',port=6379,db=0)
realtimedatarouter = APIRouter()
db_url = "postgresql://postgres:postgres@Injection-Machine-Database:5432/cax"
engine = create_engine(db_url)
Base = declarative_base()

Base = declarative_base()

@realtimedatarouter.get("/smc/injectionmachinemes/realtimedata/{machineid}")
async def insertdata(machineid:str):
    returnData       = {"status":"error","Data":{}}
    try:
        updatetime = red.get(f'{machineid}_updatetime').decode('utf-8')
        datetime_obj = datetime.strptime(updatetime, "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        time_difference = current_time - datetime_obj
        seconds_diff = time_difference.total_seconds()
        online = "Online"
        if seconds_diff > 5:
            online = "Offline"
        machinestatus   = red.get(f'{machineid}_status')
        machinestatus   = json.loads(machinestatus)
        machinefeedback = red.get(f'{machineid}_feedback')
        machinefeedback = json.loads(machinefeedback)
        machinecurve    = red.get(f'{machineid}_curve')
        machinecurve    = json.loads(machinecurve)
        resdata = {"Online":online,"machinestatus":machinestatus,"machinefeedback":machinefeedback,"machinecurve":machinecurve}
        returnData = {"status": "success","Data":resdata}
    except:
        logging.error("Get machine real time data API crashed ...")
        pass
    return returnData

@realtimedatarouter.get("/smc/injectionmachinemes/machineconnectstatus")
async def getconnectionstatus():
    returnData       = {"status":"error","Data":{}}
    try:
        sql=f'''
            select machinename from "Machinelist" where activate  = 'True'
        '''
        resdata     = {}
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                machinename = row[0]
                try:
                    updatetime = red.get(f'{machinename}_updatetime').decode('utf-8')
                    datetime_obj = datetime.strptime(updatetime, "%Y-%m-%d %H:%M:%S.%f")
                    current_time = datetime.now()
                    time_difference = current_time - datetime_obj
                    seconds_diff = time_difference.total_seconds()
                    online = "Online"
                    if seconds_diff > 5:
                        online = "Offline"
                    resdata[machinename] = online
                except:
                    online = "Offline"
                    resdata[machinename] = online
        returnData = {"status": "success","Data":resdata}
    except Exception as e:
        print(e)
        logging.error("Get machineconnectstatus data API crashed ...")
        pass
    return returnData






