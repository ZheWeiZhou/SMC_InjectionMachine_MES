from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import create_engine, Column, Integer, String,DateTime,text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import logging
import pickle
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
import pika
import json
import redis
red = redis.Redis(host='Redis',port=6379,db=0)
rabbitmq_account  = "cax"
rabbitmq_pass    = "cax521"
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)
model=''
with open('routers/model/model_file.pkl','rb') as f:
    model=pickle.load(f)

db_url = "postgresql://postgres:postgres@Injection-Machine-Database:5432/cax"
engine = create_engine(db_url)
Base = declarative_base()

troubleshootingrouter = APIRouter()
class diagnosis_requestBody(BaseModel):
    machine_name: str | None
    evidences: Any | None

class send_diagnosis_command_requestBody(BaseModel):
    machine_name: str | None
    defect: str | None
    defectlevel : str | None
    
@troubleshootingrouter.post("/smc/injectionmachinemes/troubleshooting/diagnosis")
async def diagnosis(requestData:diagnosis_requestBody):
    returnData   = {"status":"error"}
    # 射出行程/自動轉保時間   -> InjectionDoseVsFillingTime
    # 充填時間vs自動轉保時間  -> ActFillingTimeVsFillingTime
    # 射出終點VS射出位置      -> InjectionEndVsInjectionPosition
    # 料管溫度VS塑料建議溫度   -> ActBarrelTempVsSuggestTemp
    # 當前背壓vs材料建議背壓   -> BackPressureVsSuggestPressure
    # 最大射壓VS射壓設定值     -> MaxInjectionPressureVsSettingPressure
    # 射壓設定值VS機台射壓最大值 -> SettingPressureVsMachineLimitPressure
    # 射速設定值VS機台射速最大值 -> SettingSpeedVsMachineLimitSpeed
    # 實際最高射速vs射速設定最大值 ->MaxSpeedVsSpeedSetting
    # 最高射速行程占比            -> HighSpeedRatio
    # 短射                       -> ShortShot
    try:
        evidences     = requestData.evidences
        Bnetworkinput = {
            "射出行程/自動轉保時間": int(evidences["InjectionDoseVsFillingTime"]),
            "充填時間vs自動轉保時間": int(evidences["ActFillingTimeVsFillingTime"]),
            "射出終點VS射出位置": int(evidences["InjectionEndVsInjectionPosition"]),
            "料管溫度VS塑料建議溫度": int(evidences["ActBarrelTempVsSuggestTemp"]),
            "當前背壓vs材料建議背壓": int(evidences["BackPressureVsSuggestPressure"]),
            "最大射壓VS射壓設定值": int(evidences["MaxInjectionPressureVsSettingPressure"]),
            "射壓設定值VS機台射壓最大值": int(evidences["SettingPressureVsMachineLimitPressure"]),
            "射速設定值VS機台射速最大值": int(evidences["SettingSpeedVsMachineLimitSpeed"]),
            "實際最高射速vs射速設定最大值": int(evidences["MaxSpeedVsSpeedSetting"]),
            "最高射速行程占比": int(evidences["HighSpeedRatio"]),
            "短射": int(evidences["ShortShot"]),
        }
        var  = ["自動轉保時間時間過短","射速過低","射壓過低","計量不足"]
        name = ["Short Filling Time","Low Injection Speed","Low Injection Pressure","Low Injection Dose"]
        short_shot_infer = VariableElimination(model)
        q = short_shot_infer.query(variables=var,evidence=Bnetworkinput,joint =False,)
        ans={}
        for i in range(len(var)):
            key = var[i]
            enname = name[i]
            ans[enname] = q[key].values[1]
        returnData = {"status":"success","Data":ans}
    except Exception as e:
        print(e)
        pass
    return returnData
    
@troubleshootingrouter.post("/smc/injectionmachinemes/troubleshooting/send_diagnosis_command")
async def sendcommand(requestData:send_diagnosis_command_requestBody):
    returnData   = {"status":"error"}
    try:
        machinename = requestData.machine_name
        sql=f'''
            select troubleshooting from "Machinelist" where machinename  = '{machinename}' limit 1
        '''
        activate = "False"
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                activate= row[0]
        if activate == "True":
            Deffect      = requestData.defect
            DeffectLevel = requestData.defectlevel
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials(rabbitmq_account, rabbitmq_pass)
            ))
            channel = connection.channel()
            channel.queue_declare(queue=f"{machinename}_troubleshooting")
            
            commandbody = {"Deffect":Deffect,"DeffectLevel":DeffectLevel}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                        routing_key=f"{machinename}_troubleshooting",
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )
            connection.close()
            returnData = {"status": "success"}
    except Exception as e:
        print("send_diagnosis_command",e)
    return returnData


class getsloveabstract(BaseModel):
    machine_name:str
# get processline info
@troubleshootingrouter.post("/smc/injectionmachinemes/troubleshooting/getabstract")
async def checktbs(requestData:getsloveabstract):
    returnData       = {"status":"error","Data":{}}
    try:
        resdata = {}
        machinename = requestData.machine_name
        SloveAbstract = red.get(f'{machinename}_SloveAbstract')
        SloveAbstract = json.loads(SloveAbstract)
        for item in SloveAbstract["SloveAbstract"]:
            origin = json.loads(item["Origin"])
            if isinstance(origin, list):
                origin = [round(x, 1) for x in origin]
            new = json.loads(item["New"])
            if isinstance(new, list):
                new = [round(x, 1) for x in new]
            item["Origin"] = origin
            item["New"] = new
        resdata["SloveAbstract"] = SloveAbstract
        returnData       = {"status":"success","Data":resdata}
    except Exception as e:
        print(e)
        pass
    return returnData       