from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any,List
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
with open('config.json', 'r', encoding='utf-8') as f:
    envparameter = json.load(f)
red = redis.Redis(host=envparameter["red_url"],port=6379,db=0)
realtimedatarouter = APIRouter()

engine = create_engine(envparameter["db_url"])
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
                    machineworkstatus = 'Sleep'
                    if online != "Offline":
                        try:
                            machinestatus  = red.get(f'{machinename}_status')
                            machinestatus   = json.loads(machinestatus)
                            machineworkstatus = machinestatus["machine"]["value"]
                        except:
                            machineworkstatus = "NA"
                    
                    machineitem = {'Online':online,'Status':machineworkstatus}
                    resdata[machinename] = machineitem
                except:
                    machineitem = {'Online':"Offline",'Status':"Sleep"}
                    resdata[machinename] = machineitem
        returnData = {"status": "success","Data":resdata}
    except Exception as e:
        print(e)
        logging.error("Get machineconnectstatus data API crashed ...")
        pass
    return returnData

@realtimedatarouter.get("/smc/injectionmachinemes/realtimepower/{machineid}")
async def insertdata(machineid:str):
    returnData       = {"status":"error","Data":{}}
    try:
        machineenergy   = red.get(f'{machineid}_energy')
        machineenergy   = json.loads(machineenergy)
        init_power_status = red.get(f'{machineid}_init_power_status')
        if init_power_status is not None:
            init_power_status = json.loads(init_power_status)
        else:
            init_power_status = {}

        machinestatus   = red.get(f'{machineid}_status')
        machinestatus   = json.loads(machinestatus)
        holdingtimeset = machinestatus["holdingtimeset"]
        holdingpressureset = machinestatus["holdingpressureset"]
        injection_speed = machinestatus["injection_speed"]
        parameter_setting = []
        chinesemaping = ["一","二","三","四","五","六","七"]
        for i, (key, value) in enumerate(injection_speed.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段射速","unit":"mm/s"})
        for i, (key, value) in enumerate(holdingpressureset.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段保壓壓力","unit":"bar"})
        for i, (key, value) in enumerate(holdingtimeset.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段保壓時間","unit":"s"})
        machineenergy["parameter_setting"] = parameter_setting
        resdata = {"machineenergy":machineenergy,"originstatus":init_power_status}
        returnData = {"status": "success","Data":resdata}
    except:
        logging.error("Get machine energy API crashed ...")
        pass
    return returnData

class processlinestatus_requestBody(BaseModel):
    machine_name:str
# Get AOI Process Line Status
@realtimedatarouter.post("/smc/injectionmachinemes/processlinestatus")
async def getconnectionstatus(requestData:processlinestatus_requestBody):
    returnData       = {"status":"error","Data":{}}
    try:
        machine_name       = requestData.machine_name
        processlinestatus  = red.get(f'{machine_name}_Process_Line_status').decode('utf-8')
        resdata            = {"processlinestatus":processlinestatus}
        returnData = {"status": "success","Data":resdata}
    except Exception as e:
        print(e)
        logging.error("Get machineconnectstatus data API crashed ...")
        pass
    return returnData

class checktroubleshooting_requestBody(BaseModel):
    machine_name:str
# Check Machine Special module activate status
@realtimedatarouter.post("/smc/injectionmachinemes/checkmodule")
async def checktbs(requestData:checktroubleshooting_requestBody):
    returnData       = {"status":"error","Data":{}}
    try:
        machinename = requestData.machine_name
        sql=f'''
            select troubleshooting,aoimodule,powermeter from "Machinelist" where machinename  = '{machinename}' limit 1
        '''
        resdata     = {"activate":"False"}
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                resdata["troubleshooting"] = row[0]
                resdata["aoimodule"]       = row[1]
                resdata["powermeter"]      = row[2]
        returnData       = {"status":"success","Data":resdata}
    except Exception as e:
        print(e)
        pass
    return returnData



class getprocesslineinfo_requestBody(BaseModel):
    machine_name:str
# get processline info
@realtimedatarouter.post("/smc/injectionmachinemes/processlineinfo")
async def checktbs(requestData:getprocesslineinfo_requestBody):
    returnData       = {"status":"error","Data":{}}
    try:
        resdata = {}
        machinename = requestData.machine_name
        processlinemessage = red.get(f'{machinename}_Process_Line_message')
        processlinemessage = json.loads(processlinemessage)
        resdata["processlinemessage"] = processlinemessage
        returnData       = {"status":"success","Data":resdata}
    except Exception as e:
        print(e)
        pass
    return returnData        

@realtimedatarouter.get("/smc/injectionmachinemes/currentcurve/{machineid}")
async def insertdata(machineid:str):
    returnData       = {"status":"error","Data":{}}
    try:
        curve   = red.get(f'PowerMeter_{machineid}_curve')
        if curve:
            curve   = json.loads(curve)
        else:
            curve = {
                "current_a":  [-1],
                "current_b":  [-1],
                "current_c":  [-1],
            }
        resdata = {"current":curve}
        returnData = {"status": "success","Data":resdata}
    except:
        logging.error("Get machine currentcurve crashed ...")
        pass
    return returnData

class updatepowerinfo_requestBody(BaseModel):
    machine_name:str
    curve:Dict[str, Any] = {}
    abstract:Dict[str, Any] = {}
    cal:List[Dict[str, Any]] = []
    powerprediction:List[Dict[str, Any]] = []
    expectation:List[Dict[str, Any]] = []
@realtimedatarouter.post("/smc/injectionmachinemes/updatemachinepowerdata")
async def updatepowerinfo(requestData:updatepowerinfo_requestBody):
    returnData       = {"status":"error"}
    try:
        machine_id = requestData.machine_name
        curve = requestData.curve
        abstract = requestData.abstract
        cal = requestData.cal
        powerprediction = requestData.powerprediction
        expectation = requestData.expectation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        machinepowerinfo ={}
        # Get Machine Setting Parameter
        machinepowerinfo["updatetime"] = current_time
        machinepowerinfo["abstract"] = abstract
        machinepowerinfo["curve"] = curve
        machinepowerinfo["cal"] = cal
        # 用當前機台參數算出來的能耗預測值
        machinepowerinfo["powerprediction"] = powerprediction
        # 用優化參數算出來的能耗預測值
        machinepowerinfo["expectation"] = expectation 
        red.set(f'{machine_id}_energy',json.dumps(machinepowerinfo))
        machinestatus   = red.get(f'{machine_id}_status')
        machinestatus   = json.loads(machinestatus)
        init_power_status = red.get(f'{machine_id}_init_power_status')
        holdingtimeset = machinestatus["holdingtimeset"]
        holdingpressureset = machinestatus["holdingpressureset"]
        injection_speed = machinestatus["injection_speed"]
        parameter_setting = []
        chinesemaping = ["一","二","三","四","五","六","七"]
        for i, (key, value) in enumerate(injection_speed.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段射速","unit":"mm/s"})
        for i, (key, value) in enumerate(holdingpressureset.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段保壓壓力","unit":"bar"})
        for i, (key, value) in enumerate(holdingtimeset.items()):
            if float(value['value'])>0:
                parameter_setting.append({"nodename":key,"value":value['value'],"name":f"第{chinesemaping[i]}段保壓時間","unit":"s"})
        red.set(f'{machine_id}_energy',json.dumps(machinepowerinfo))
        if init_power_status is None:
            original_step = {
                "abstract":abstract,
                "parameter_setting":parameter_setting,
                "updatetime":current_time
            }
            red.set(f'{machine_id}_init_power_status',json.dumps(original_step))
        returnData = {"status":"success"}
    except Exception as e:
        print(f"發生錯誤了：{e}")
    return returnData


class reset_originalPowerinfo_requestBody(BaseModel):
    machine_name:str
@realtimedatarouter.post("/smc/injectionmachinemes/resetpowerfirststep")
async def resetpowerinfo(requestData:reset_originalPowerinfo_requestBody):
    returnData       = {"status":"error"}
    try:
        machine_id = requestData.machine_name
        resetresult = red.delete(f'{machine_id}_init_power_status')
        if resetresult == 1:
            returnData = {"status":"success"}
    except:
        pass
    return returnData

@realtimedatarouter.get("/smc/injectionmachinemes/pvtcurve/{machineid}")
async def insertdata(machineid:str):
    returnData       = {"status":"error","Data":{}}
    try:
        curve   = red.get(f'{machineid}_pvt')
        if curve:
            curve   = json.loads(curve)
        else:
            curve = {
                "P1":  [],
                "P2":  [],
                "P3":  [],
                "T1":  [],
                "T2":  [],
                "T3":  [],
                "V_support_0":[],
                "V_support_50":[],
                "V_support_100":[],
                "updatetime":''
            }
        resdata = {"current":curve}
        returnData = {"status": "success","Data":resdata}
    except:
        logging.error("Get machine pvtcurve crashed ...")
        pass
    return returnData

