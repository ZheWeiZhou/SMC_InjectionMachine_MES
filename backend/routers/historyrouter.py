from fastapi import APIRouter, Request
from typing import Dict, Any
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime,text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import json
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)


historyrouter = APIRouter()

db_url = "postgresql://postgres:postgres@Injection-Machine-Database:5432/cax"
engine = create_engine(db_url)
Base = declarative_base()

class MachineHistory(Base):
    __tablename__ = 'MachineHistory'
    id = Column(Integer,primary_key=True)
    machine_name = Column(String)
    machine_setting = Column(String)
    machine_feedback = Column(String)
    machine_curve = Column(String)

class BayesianNetworkTrainData(Base):
    __tablename__ = 'BayesianNetworkTrainData'
    id = Column(Integer,primary_key=True)
    machinehistoryid = Column(Integer)
    machine_name = Column(String)
    model_result = Column(String)

class inserthistorydata_requestBody(BaseModel):
    machine_name:str
    machine_setting:str
    machine_feedback:str
    machine_curve:str

class insertBayesianData_requestBody(BaseModel):
    machine_name:str
    modelresult:str
    abstract: Any | None

class getHistoryData_requestBody(BaseModel):
    machine_name:str
    start_time:str
    end_time:str

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
@historyrouter.post("/smc/injectionmachinemes/history/insertBayesianNetworkTrainData")
async def insertBayesianData(requestData:insertBayesianData_requestBody):
    returnData       = {"status":"error"}
    mappingtable     =  {"自動轉保時間時間過短":"LowFlTime","射速過低":"LowSpeed","射壓過低":"LowPressure","計量不足":"LowDose","背壓過低":"LowBackPressure"}
    mappingtable_Key = list(mappingtable.keys())
    try:
        MachineName         = requestData.machine_name
        LatestMachineDataID = []
        sql=f'''
            SELECT id FROM "MachineHistory" WHERE machine_name = '{MachineName}' ORDER BY id DESC Limit 1
        '''
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                LatestMachineDataID = [row[0]]
        Modelresult    = requestData.modelresult
        Modelresult    = Modelresult.split(",")
        Modelresult_EN = []
        for i in Modelresult :
            if i in mappingtable_Key:
                Modelresult_EN.append(mappingtable[i])
        Adjustabstract   = requestData.abstract
        storagedata      = {"Modelresult":Modelresult_EN,"SloveAbstract":Adjustabstract}
        storagedata      = json.dumps(storagedata)
        MachineHistoryID = LatestMachineDataID[0]
        Session          = sessionmaker(bind=engine)
        session          = Session()
        insert_sql=BayesianNetworkTrainData.__table__.insert().values(
            machinehistoryid = MachineHistoryID,
            machine_name     = MachineName,
            model_result     = storagedata,
        )
        session.execute(insert_sql)
        session.commit()
        session.close()
        returnData      = {"status":"success"}
    except Exception as e:
        print(e)
    return returnData
def parsestatusdata(data,item):
    for variable in list(item.keys()):
        print(variable)
        if isinstance(item[variable], dict):
            if 'value' in item[variable]:
                if variable not in list(data.keys()):
                    data[variable] = [item[variable]['value']]
                else:
                    data[variable].append(item[variable]['value'])
            else :
                for child_variable in list(item[variable].keys()):
                    if child_variable not in data:  
                        data[child_variable] = [item[variable][child_variable]['value']]
                    else:
                        data[child_variable].append(item[variable][child_variable]['value'])
    return data
         
def parsefeedbackdata(data,item):
    for variable in list(item.keys()):
        if variable not in list(data.keys()):
            data[variable] = [item[variable]]
        else:
            data[variable].append(item[variable])
    return data     

@historyrouter.post("/smc/injectionmachinemes/history/getdata")
async def gethistorydata(requsetData:getHistoryData_requestBody):
    returnData       = {"status":"error"}
    try:
        data      = {'id':[],'created_at':[],'machine_name':[]}
        curvedata = {} 
        MachineName = requsetData.machine_name
        start_time  = requsetData.start_time
        end_time    = requsetData.end_time
        sql = f'''SELECT id,created_at,machine_name,machine_status,machine_feedback,machine_curve FROM "MachineHistory" WHERE machine_name = '{MachineName}' and created_at > '{start_time}' and created_at < '{end_time}'  ORDER BY id DESC'''
        with engine.connect() as connection:
                result = connection.execute(text(sql))
                for row in result.mappings():
                    dataid           = row['id']
                    created_at       = row['created_at']
                    machine_name     = row['machine_name']
                    data['id'].append(dataid)
                    data['created_at'].append(created_at)
                    data['machine_name'].append(machine_name)
                    machine_status   = row['machine_status']
                    machine_status   = json.loads(machine_status)
                    data             = parsestatusdata(data,machine_status)
                    machine_feedback = row['machine_feedback']
                    machine_feedback = json.loads(machine_feedback)
                    data             = parsefeedbackdata(data,machine_feedback)
                    machine_curve    = row['machine_curve']
                    machine_curve    = json.loads(machine_curve)
                    curvedata        = parsefeedbackdata(curvedata,machine_curve)
        rsdata = {"variable":data,"curve":curvedata}
        returnData = {"status":"success","Data":rsdata}
    except Exception as e:
        print(e)
    return returnData





