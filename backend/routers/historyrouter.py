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






