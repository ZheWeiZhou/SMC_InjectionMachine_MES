from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import pickle
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)
import pickle
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
import json
model=''
with open('routers/model/model_file.pkl','rb') as f:
    model=pickle.load(f)

troubleshootingrouter = APIRouter()
class diagnosis_requestBody(BaseModel):
    machine_name: str | None
    evidences: Any | None
    
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
        evidences = requestData.evidences
        # evidences = json.loads(evidences)
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
        var = ["自動轉保時間時間過短","射速過低","射壓過低","計量不足","背壓過低"]
        short_shot_infer = VariableElimination(model)
        q = short_shot_infer.query(variables=var,evidence=Bnetworkinput,joint =False,)
        ans={}
        for i in var:
            ans[i]=q[i].values[1]
        returnData = {"status":"success","Data":ans}
    except Exception as e:
        print(e)
        pass
    return returnData
    


