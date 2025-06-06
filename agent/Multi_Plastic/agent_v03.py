from aphyt import omron
# import json
# import numpy as np
# import math
# import datetime
# import time
# import re
# import redis
# import random
from sqlalchemy import create_engine, Column, Integer, String,DateTime,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# # from keras import models
# # import tensorflow as tf
# # from sklearn import preprocessing
# import pickle
# # import dataprocess_function
# from pgmpy.inference import VariableElimination
# from Process_line import Process_line_agent
# import ast
# from joblib import load
# from mettler_toledo_device import MettlerToledoDevice
# import random
# import copy
# import aiohttp, asyncio
# from dotenv import load_dotenv
# import os
db_url="postgresql://postgres:cax521@127.0.0.1:5433/postgres"
engine = create_engine(db_url)
Base = declarative_base()
# Bayesmodel=''
# with open('model_file.pkl','rb') as f:
#     Bayesmodel=pickle.load(f)
def processlinereset(weightmeter):
    processline_agent.write_batchregister(4,118,1) #切換成地0個job
    processline_agent.write_singleregister(4,125,32)#先把指令reset成stop
    processline_agent.write_singleregister(4,125,16)#命賦歸
    processline_agent.write_batchregister(3,118,0) #切換成地0個job
    processline_agent.write_singleregister(3,125,32)#先把指令reset成stop
    processline_agent.write_singleregister(3,125,8)#命令job作動
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.3)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    processline_agent.write_batchregister(3,118,2) #切換成地0個job
    processline_agent.write_singleregister(3,125,32)#先把指令reset成stop
    processline_agent.write_singleregister(3,125,8)#命令job作動
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.5)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    processline_agent.write_batchregister(3,118,3) #切換成地0個job
    processline_agent.write_singleregister(3,125,32)#先把指令reset成stop
    processline_agent.write_singleregister(3,125,8)#命令job作動
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.5)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    processline_agent.write_batchregister(3,118,4) #切換成地0個job
    processline_agent.write_singleregister(3,125,32)#先把指令reset成stop
    processline_agent.write_singleregister(3,125,8)#命令job作動
    weightreset=0
    while weightreset==0:
        time.sleep(0.5)
        weightmeter.zero_stable()
        weight=weightmeter.get_weight()[0]
        if abs(weight) <0.1:
            weightreset=1
            print('Weight meter success reset')
    
def processlinemove(BPNNresult):
    #產品移到要被分類的地方
    agent.AOI_Prediction=''
    processline_agent.write_batchregister(3,118,0)
    processline_agent.write_singleregister(3,125,32)
    processline_agent.write_singleregister(3,125,8)
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.3)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    figname,figdecode,AOIresult,visionshortshotratio=processline_agent.capturefig()
    print(f'[TEST NEW FUNCTION] SHORTSHOT VISION RATIO : {visionshortshotratio}')
    agent.red.set('AOI_predict_result',AOIresult)
    processline_agent.write_batchregister(3,118,1)
    processline_agent.write_singleregister(3,125,32)
    processline_agent.write_singleregister(3,125,8)
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.5)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    #根據AOI & BPNN 預測結果分類
    if BPNNresult==AOIresult and BPNNresult=='normal':
        print("DEBUG IN TYPE C")
        classfication('c')
    elif  BPNNresult==AOIresult and BPNNresult=='shortshot':
        classfication('b')
    else :
        classfication('a')
    print("[DEBUG] after class")
    #撥下去
    processline_agent.write_batchregister(4,118,0)
    processline_agent.write_singleregister(4,125,32)
    processline_agent.write_singleregister(4,125,8)
    waitcount=0
    
    jobfinish=0
    while jobfinish==0:
        time.sleep(0.5)
        waitcount+=1
        result=processline_agent.readsingle_register(4,127)
        if int(result[0])==8  or waitcount>15: #觀察job是否完成
            jobfinish=1
    #產線那隻復歸
    processline_agent.write_batchregister(3,118,2)
    processline_agent.write_singleregister(3,125,32)
    processline_agent.write_singleregister(3,125,8)
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.5)
        result=processline_agent.readsingle_register(3,127)
        waitcount+=1
        if int(result[0])==8 or waitcount>15: #觀察job是否完成
            jobfinish=1
    #撥桿復歸
    processline_agent.write_batchregister(4,118,1)
    processline_agent.write_singleregister(4,125,32)
    processline_agent.write_singleregister(4,125,8)
    processline_agent.write_batchregister(3,118,3)
    processline_agent.write_singleregister(3,125,32)
    processline_agent.write_singleregister(3,125,8)
    jobfinish=0
    waitcount=0
    while jobfinish==0:
        time.sleep(0.3)
        result=processline_agent.readsingle_register(3,127)
        # waitcount+=1
        if int(result[0])==8 or waitcount>20: #觀察job是否完成
            jobfinish=1
    processline_agent.write_batchregister(3,118,4)
    processline_agent.write_singleregister(3,125,32)
    processline_agent.write_singleregister(3,125,8)
    
    return figname,figdecode,visionshortshotratio
def classfication(type): #分類
    if type=='a':
        processline_agent.write_batchregister(2,118,0)
        processline_agent.write_singleregister(2,125,32)
        processline_agent.write_singleregister(2,125,8)
        processline_agent.write_batchregister(1,118,0)
        processline_agent.write_singleregister(1,125,32)
        processline_agent.write_singleregister(1,125,8)
        b=0
        while b==0:
            result1=processline_agent.readsingle_register(2,127)
            result2=processline_agent.readsingle_register(1,127)
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
    if type=='b':
        print("[DEBUG] IN type B")
        processline_agent.write_batchregister(2,118,0)
        processline_agent.write_singleregister(2,125,32)
        processline_agent.write_singleregister(2,125,8)
        processline_agent.write_batchregister(1,118,1)
        processline_agent.write_singleregister(1,125,32)
        processline_agent.write_singleregister(1,125,8)
        b=0
        while b==0:
            result1=processline_agent.readsingle_register(2,127)
            result2=processline_agent.readsingle_register(1,127)
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
                print("[DEBUG] Finish type B")
    if type=='c':
        print("[DEBUG] IN  FUNCTION type C 0")
        processline_agent.write_batchregister(2,118,1)
        processline_agent.write_singleregister(2,125,32)
        processline_agent.write_singleregister(2,125,8)
        processline_agent.write_batchregister(1,118,1)
        processline_agent.write_singleregister(1,125,32)
        processline_agent.write_singleregister(1,125,8)
        print("[DEBUG] IN  FUNCTION type C 1")
        b=0
        while b==0:
            result1=processline_agent.readsingle_register(2,127)
            result2=processline_agent.readsingle_register(1,127)
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
    print("[DEBUG] finish class")
class injection_machine_DB(Base):
    __tablename__ = 'injection_machine'
    id = Column(Integer, primary_key=True)
    injection_speed_set=Column(String(255))
    injection_pressure_set=Column(String(255))
    real_injection_speed=Column(TEXT)
    real_injection_pressure=Column(TEXT)
    holding_pressure=Column(String(255))
    vp=Column(String(255))
    vp_pressure=Column(String(255))
    clamping_force=Column(String(255))
    holding_time=Column(String(255))
    barrel_temperature=Column(String(255))
    injection_position=Column(String(255))
    max_injection_pressure=Column(String(255))
    injection_end_position=Column(String(255))
    max_holding_pressure=Column(String(255))
    filling_time=Column(String(255))
    ij_date=Column(DateTime)
    store_postion=Column(String(255))
    back_postion=Column(String(255))
    cooling_time=Column(String(255))
    back_pressure=Column(String(255))
    fillingtimelimt=Column(String(255))
    maxinjectionspeed=Column(String(255))
    bpnn_shortshot_prediction=Column(String(255))
    shortshot_reason=Column(String(255))
    aoibase64=Column(String(255))
    aoifigname=Column(String(255))
    aoi_shortshot_prediction=Column(String(255))
    weight=Column(String(255))


class injection_machine_class:
    def __init__(
            self,
            ip:str,
    ):
        self.ip=ip
        currentversion=os.getenv('bpnnmodelversion')
        self.model=models.load_model(f'shortshotpredictionV{currentversion}.h5', compile=False)
        self.normalize=load(f'normalizeV{currentversion}.joblib')
        self.red=redis.Redis(host='localhost',port=6379,db=0)
        self.process_count=0
        self.realspeed=[]
        self.realpressure=[]
        self.holdingstart_time=0
        self.process_ongoing=0  #製程開始
        self.holding_ongoning=0 #保壓開始
        self.holding_start_point=0 #當前的序列資料是從哪裡開始是保壓階段
        self.store_start=0 #是否開始儲料
        self.client=omron.n_series.NSeries()
        self.ParametersChangeSettings={'speed_choose':1,'pressure_choose':1,'holdingpressure_choose':1,
                     'holdingtime_choose':1,'clampingforce_choose':1,'fillingtimelimit_choose':1,'postion_set':1}
        self.Bayesmodel=Bayesmodel
        self.weightmeter=MettlerToledoDevice(port='COM6')
        self.AOI_Prediction=''
    def modelupdate(self):
        currentversion=os.getenv('bpnnmodelversion')
        self.model=models.load_model(f'shortshotpredictionV{currentversion}.h5', compile=False)
        self.normalize=load(f'normalizeV{currentversion}.joblib')  
    def connect(self):
        try:
            self.client.connect_explicit(self.ip)
            self.client.register_session()
            self.client.update_variable_dictionary()
            self.red.set('product_weight','0')
            self.red.set('imagecode','0')
            self.red.set('BPNN_predict_result','')
            self.red.set('shortshotreason','')
            print('Connect Success')
            # processlinereset()
            # print('Reset finish')

        except:
            print('connect failed')
    def random_setting_parameter(self):
        ParametersChangeSettings=self.red.get('ParametersChangeSettings').decode('utf-8')
        ParametersChangeSettings=json.loads(ParametersChangeSettings)#從redis讀取欲變動的參數
        # set parameter range
        speed_range=list(range(10,141,10))
        pressure_range=list(range(300,1401,100))
        holdingpressure_range=list(range(200,1401,100))
        holdingtime_range=list(range(0,4,1))
        clampingforce=list(range(40,101,5))
        fillingtimelimit=list(range(1,6,1))
        dose_range=list(range(13,19,1))
        #random choose
        # 多段射速設定----
        # speed_choose=random.sample(speed_range,5)
        # speed_choose=[float(i) for i in speed_choose]
        # -----
        # 單一射速設定----
        speed_choose=random.sample(speed_range,1)
        speed_choose=[float(speed_choose[0])]*5
        # -----
        pressure_choose=random.sample(pressure_range,1)
        pressure_choose=[float(i) for i in pressure_choose]
        holdingpressure_choose=random.sample(holdingpressure_range,2)
        holdingpressure_choose=[float(i) for i in holdingpressure_choose]
        holdingtime_choose=random.sample(holdingtime_range,2)
        holdingtime_choose=[float(i) for i in holdingtime_choose]
        clampingforce_choose=random.sample(clampingforce,1)
        clampingforce_choose=[float(i) for i in clampingforce_choose]
        fillingtimelimit_choose=random.sample(fillingtimelimit,1)
        fillingtimelimit_choose=[float(i) for i in fillingtimelimit_choose]
        dose_choose=random.sample(dose_range,1)
        dose=26-dose_choose[0]
        postion_set=np.linspace(26,dose,5).tolist()
        postion_set=[float(i) for i in postion_set]
        Parameter_selection={
            'ijpressure_input':pressure_choose,'ijspeed_input':speed_choose,'holding_pressure_input':holdingpressure_choose,
            'holding_time_input':holdingtime_choose,'clamping_force_input':clampingforce_choose,'coolingtime_input':None,
            'fillingtimelimit_input':fillingtimelimit_choose,'injection_postion_input':postion_set
        }
        # for k in Parameter_selection:
        #     if k not in ParametersChangeSettings.keys():
        #         Parameter_selection[k]=None
        for k in ParametersChangeSettings.keys():
            if ParametersChangeSettings[k]==0:
                Parameter_selection[k]=None
        # for k in self.ParametersChangeSettings.keys():
        #     print(self.ParametersChangeSettings[k],type(self.ParametersChangeSettings[k]))
        #     if int(self.ParametersChangeSettings[k])==0:
        #         Parameter_selection[k]=None
        # print('Parameter_selection',Parameter_selection)
        self.set_parameter(Parameter_selection)

    def set_parameter(self,input):
        # set ijpressure
        if input['ijpressure_input'] != None:
            injection_pressure_setting=self.client.read_variable('PD_IN_HMI')
            injection_pressure_setting[0]=input['ijpressure_input'][0]           
            self.client.write_variable('PD_IN_HMI',injection_pressure_setting)
        # set ij speed
        if input['ijspeed_input'] != None:
            injection_speed_setting=self.client.read_variable('FD_IN_HMI')#射速設定值
            injection_speed_setting[:5]=input['ijspeed_input']
            self.client.write_variable('FD_IN_HMI',injection_speed_setting)
        # set holding pressure
        if input['holding_pressure_input'] !=None:
            holding_pressure_setting=self.client.read_variable('PD_HD_HMI')#保壓時間
            # 機台是有3段保壓，但我只用2段
            holding_pressure_setting[:2]=input['holding_pressure_input']
            self.client.write_variable('PD_HD_HMI',holding_pressure_setting)
        # set holding time
        if input['holding_time_input'] !=None:
            holding_time_setting=self.client.read_variable('ST_HD_HMI')#保壓時間
            # 機台是有3段保壓，但我只用2段
            holding_time_setting[:2]=input['holding_time_input']
            self.client.write_variable('ST_HD_HMI',holding_time_setting)
        # set clamping force
        if input['clamping_force_input'] !=None:
            clamping_force=self.client.read_variable('FD_MC_HMI')#鎖模力(%)
            clamping_force[4]=input['clamping_force_input'][0]
            self.client.write_variable('FD_MC_HMI',clamping_force)
        # set cooling time
        if input['coolingtime_input'] != None:
            coolingtime=self.client.read_variable('ST_HD_HMI')#冷卻時間
            coolingtime[6]=input['coolingtime_input'][0]
            self.client.write_variable('ST_HD_HMI',coolingtime)
        # set fillingtimelimit
        if input['fillingtimelimit_input'] !=None:
            fillingtimelimt=self.client.read_variable('ST_IN_HMI')#自動轉保時間
            fillingtimelimt[0]=input['fillingtimelimit_input'][0]
            self.client.write_variable('ST_IN_HMI',fillingtimelimt)
        #set injection postion
        if input['injection_postion_input'] !=None:
            injection_postion=self.client.read_variable('SP_IN_HMI')#射出位置
            injection_postion[:5]=input['injection_postion_input']
            print('injection_postion',injection_postion)
            self.client.write_variable('SP_IN_HMI',injection_postion)
    def collect_data(self):
        thersold_of_parameter_change=int(self.red.get('thersold_of_parameter_change').decode('utf-8')) #每幾模更改參數
        random_parameter_setting=int(self.red.get('random_parameter_setting').decode('utf-8')) #是否執行隨機設置參數機制
        moldclose=self.client.read_variable('Y23B')#是否合模
        respeed=self.client.read_variable('D_MA_HMI')[6]#當前射出速度
        respeed=math.floor(respeed * 100)/100.0
        holdingstart=self.client.read_variable('MOVEFWD_STEP_IN')[25]#保壓開始
        if moldclose is True and respeed !=0:
            self.process_ongoing=1
            self.red.set('product_weight','0')
            self.red.set('imagecode','0')
            self.red.set('fillingratio','0')
            if self.store_start==0:
                #清空BPNN預測結果
                self.red.set('process_ongoing','1')#更新redis現在射出機正在充填
                self.red.set('BPNN_predict_result','')
                self.red.set('AOI_predict_result','')
                self.red.set('shortshotreason','')
                self.realspeed.append(respeed)
                repressure=self.client.read_variable('D_MA_HMI')[18]#當前射出壓力
                repressure=math.floor(repressure * 100)/100.0
                self.realpressure.append(repressure)
                # upload realpressure and realspeed to redis
                self.red.rpush('realspeed',str(respeed))
                self.red.rpush('realpressure',str(repressure))
            if holdingstart is True and self.holding_ongoning==0:
                self.holding_ongoning=1
                self.holding_start_point=len(self.realspeed)
            if len(self.realspeed) >3 and self.store_start==0:
                check=[self.realspeed[-3],self.realspeed[-2],self.realspeed[-1]]
                if sum(check) <0:
                    print('[INFO] Start to store material..')
                    self.store_start=1
                    # process setting parameter
                    injection_pressure_setting=self.client.read_variable('PD_IN_HMI')[0]#射壓設定值                    
                    injection_speed_setting=self.client.read_variable('FD_IN_HMI')[:5]#射速設定值
                    injection_speed_setting=[math.floor(a * 100)/100.0 for a in injection_speed_setting] 
                    injection_postion_setting=self.client.read_variable('SP_IN_HMI')[:5]#射出位置
                    injection_postion_setting=[math.floor(a * 100)/100.0 for a in injection_postion_setting]
                    store_postion=self.client.read_variable('SP_ME_HMI')[:2]#除料位置
                    back_postion=self.client.read_variable('SP_SB_HMI')[2]#後松退
                    barrel_temperature_setting=self.client.read_variable('S_TE_HMI')[:5]#料管溫度設定
                    holding_time_setting=self.client.read_variable('ST_HD_HMI')[:4]#保壓時間
                    holding_time_setting=[math.floor(a * 100)/100.0 for a in holding_time_setting]
                    VP_postion=self.client.read_variable('D_SPC_SAVE')[1]#VP點
                    clamping_force=self.client.read_variable('FD_MC_HMI')[4]#鎖模力(%)
                    holdingset=self.client.read_variable('PD_HD_HMI')[:3]#保壓
                    coolingtime=self.client.read_variable('ST_HD_HMI')[6]#冷卻時間
                    coolingtime=math.floor(coolingtime * 100)/100.0
                    fillingtimelimt=self.client.read_variable('ST_IN_HMI')[0]#自動轉保時間
                    backpressure=self.client.read_variable('PD_ME_HMI')[2:4]#suckbackpressure
                    # process analysis
                    vp_pressure=self.client.read_variable('D_SPC_SAVE')[9]#VP轉換壓
                    max_holding_pressure=self.client.read_variable('SPC_PD_HD')[1]#保壓峰值
                    End=self.client.read_variable('D_MA_HMI')[15]#射出終點
                    End=math.floor(End * 100)/100.0
                    fillingtime=self.client.read_variable('D_SPC_SAVE')[5]#充填時間
                    fillingtime=self.client.read_variable('D_SPC_SAVE')[5]#充填時間
                    maxinjectionpressure=0
                    maxinjectionspeed=0
                    if self.holding_ongoning==1:
                        maxinjectionpressure=max(self.realpressure[:self.holding_start_point+1])
                        maxinjectionspeed=max(self.realspeed[:self.holding_start_point+1])
                    else:
                        maxinjectionpressure=max(self.realpressure)
                        maxinjectionspeed=max(self.realspeed)
                    # upload to redis --process setting parameter
                    self.red.set('injection_pressure_setting',str(injection_pressure_setting))
                    self.red.set('injection_speed_setting',str(injection_speed_setting))
                    self.red.set('injection_postion_setting',str(injection_postion_setting))
                    self.red.set('store_postion',str(store_postion))
                    self.red.set('back_postion',str(back_postion))
                    self.red.set('barrel_temperature_setting',str(barrel_temperature_setting))
                    self.red.set('VP_postion',str(VP_postion))
                    self.red.set('clamping_force',str(clamping_force))
                    self.red.set('holdingset',str(holdingset))
                    self.red.set('coolingtime',str(coolingtime))
                    self.red.set('fillingtimelimt',str(fillingtimelimt))
                    self.red.set('holding_time_setting',str(holding_time_setting))
                    # upload to redis --process analysis
                    self.red.set('vp_pressure',str(vp_pressure))
                    self.red.set('max_holding_pressure',str(max_holding_pressure))
                    self.red.set('End',str(End))
                    self.red.set('fillingtime',str(fillingtime))
                    self.red.set('maxinjectionpressure',str(maxinjectionpressure))
                    self.red.set('maxinjectionspeed',str(maxinjectionspeed))
                    self.red.set('backpressure',str(backpressure))
                    # upload to redis --ij speed & pressure curve
                    #預測短射
                    prediction=self.predict()
                    #upload model predict result
                    self.red.set('BPNN_predict_result',prediction)
                    #短射分析
                    if prediction=='shortshot':
                        short_shot_reason=self.short_shot_analyis()
                        short_shot_reason=json.dumps(short_shot_reason)
                        self.red.set('shortshot_reason',short_shot_reason)
        elif moldclose is False and self.process_ongoing==1:
            #這邊要執行讓產線動起來的動作==============================
            BPNNresult=self.red.get('BPNN_predict_result').decode('utf-8')
            print("[INFO] know mold open start to count")
            time.sleep(35)
            print("[INFO] activate process line")
            productweight=0
            for i in range(3):
                try:
                    productweight=self.weightmeter.get_weight()[0]
                    if isinstance(productweight, float):
                        break
                except:
                    pass
            self.red.set('product_weight',productweight)
            weightratio=productweight/19
            check =self.red.get('product_weight').decode('utf-8')
            figname,figdecode,visionfillingratio=processlinemove(BPNNresult) #會回傳AOI照片的base64 跟figname
            fillingratio=0.5*visionfillingratio+0.5*weightratio
            self.red.set('fillingratio',fillingratio)
            self.figname=figname
            self.figdecode=figdecode
            self.red.set('imagecode',figdecode)
            #========================================================
            self.process_ongoing=0
            self.store_start=1
            self.realspeed=[]
            self.realpressure=[]
            self.holding_ongoning=0 #保壓開始
            self.holding_start_point=0 #當前的序列資料是從哪裡開始是保壓階段
            self.store_start=0 #是否開始儲料
            self.process_count+=1
            # Auto defect resolution 
            AutoDefectResolution=int(self.red.get('AutoDefectResolution').decode('utf-8'))
            if AutoDefectResolution ==1:
                bpnnpredict=self.red.get('BPNN_predict_result').decode('utf-8')
                AOIresult=self.red.get('AOI_predict_result').decode('utf-8')
                if bpnnpredict=='shortshot' or AOIresult=='shortshot':
                    print('[System INFO] Start to Auto Defect Resolution....')
                    shortshotreason=self.red.get('shortshotreason').decode('utf-8')
                    shortshotreason=json.loads(shortshotreason)
                    self.shortshotresolution(shortshotreason,fillingratio)
            #store data to db
            self.store_data()
            self.red.delete('realspeed')
            self.red.delete('realpressure')
            if self.process_count==thersold_of_parameter_change:
                if random_parameter_setting==1:
                    self.random_setting_parameter()
                self.process_count=0
        else:
            self.figname=0
            self.figdecode=0
            injection_pressure_setting=self.client.read_variable('PD_IN_HMI')[0]#射壓設定值
            injection_speed_setting=self.client.read_variable('FD_IN_HMI')[:5]#射速設定值
            injection_speed_setting=[math.floor(a * 100)/100.0 for a in injection_speed_setting] 
            injection_postion_setting=self.client.read_variable('SP_IN_HMI')[:5]#射出位置
            injection_postion_setting=[math.floor(a * 100)/100.0 for a in injection_postion_setting]
            store_postion=self.client.read_variable('SP_ME_HMI')[:2]#除料位置
            back_postion=self.client.read_variable('SP_SB_HMI')[2]#後松退
            barrel_temperature_setting=self.client.read_variable('S_TE_HMI')[:5]#料管溫度設定
            holding_time_setting=self.client.read_variable('ST_HD_HMI')[:4]#保壓時間
            holding_time_setting=[math.floor(a * 100)/100.0 for a in holding_time_setting]
            VP_postion=self.client.read_variable('D_SPC_SAVE')[1]#VP點
            clamping_force=self.client.read_variable('FD_MC_HMI')[4]#鎖模力(%)
            holdingset=self.client.read_variable('PD_HD_HMI')[:3]#保壓
            coolingtime=self.client.read_variable('ST_HD_HMI')[6]#冷卻時間
            coolingtime=math.floor(coolingtime * 100)/100.0
            fillingtimelimt=self.client.read_variable('ST_IN_HMI')[0]#自動轉保時間
            backpressure=self.client.read_variable('PD_ME_HMI')[2:4]#suckbackpressure

            # upload to redis
            if moldclose is False:
                self.red.set('process_ongoing',str(0)) #更新redis現在射出機處於閒置狀態 
            self.red.set('injection_pressure_setting',injection_pressure_setting)
            self.red.set('injection_speed_setting',str(injection_speed_setting))
            self.red.set('injection_postion_setting',str(injection_postion_setting))
            self.red.set('store_postion',str(store_postion))
            self.red.set('back_postion',str(back_postion))
            self.red.set('barrel_temperature_setting',str(barrel_temperature_setting))
            self.red.set('VP_postion',str(VP_postion))
            self.red.set('clamping_force',str(clamping_force))
            self.red.set('holdingset',str(holdingset))
            self.red.set('coolingtime',str(coolingtime))
            self.red.set('fillingtimelimt',str(fillingtimelimt))
            self.red.set('holding_time_setting',str(holding_time_setting))
            self.red.set('backpressure',str(backpressure))
    async def store_data(self):
        injection_speed_setting=self.red.get('injection_speed_setting').decode('utf-8')
        injection_pressure_setting=self.red.get('injection_pressure_setting').decode('utf-8')
        raw_real_injection_speed=self.red.lrange('realspeed',0,-1)
        clean_injection_speed=[]
        for i in raw_real_injection_speed:
            clean_injection_speed.append(float(i.decode('utf-8')))
        raw_real_injection_pressure=self.red.lrange('realpressure',0,-1)
        clean_injection_pressure=[]
        for i in raw_real_injection_pressure:
            clean_injection_pressure.append(float(i.decode('utf-8')))
        holdingset=self.red.get('holdingset').decode('utf-8')
        VP_postion=self.red.get('VP_postion').decode('utf-8')
        vp_pressure=self.red.get('vp_pressure').decode('utf-8')
        clamping_force=self.red.get('clamping_force').decode('utf-8')
        holding_time_setting=self.red.get('holding_time_setting').decode('utf-8')
        barrel_temperature_setting=self.red.get('barrel_temperature_setting').decode('utf-8')
        injection_postion_setting=self.red.get('injection_postion_setting').decode('utf-8')
        maxinjectionpressure=self.red.get('maxinjectionpressure').decode('utf-8')
        End=self.red.get('End').decode('utf-8')
        max_holding_pressure=self.red.get('max_holding_pressure').decode('utf-8')
        fillingtime=self.red.get('fillingtime').decode('utf-8')
        store_Postion=self.red.get('store_postion').decode('utf-8')
        back_postion=self.red.get('back_postion').decode('utf-8')
        coolingtime=self.red.get('coolingtime').decode('utf-8')
        backpressure=self.red.get('backpressure').decode('utf-8')
        fillingtimelimt=self.red.get('fillingtimelimt').decode('utf-8')
        maxinjectionspeed=self.red.get('maxinjectionspeed').decode('utf-8')
        BPNN_shortshot_predict=self.red.get('BPNN_predict_result').decode('utf-8')
        weight=self.red.get('product_weight').decode('utf-8')
        fillingratio=self.red.get('fillingratio').decode('utf-8')
        shortshotreason_todb=[]
        aoibase64=self.figdecode
        aoifigname=self.figname
        try:
            shortshotreason=self.red.get('shortshotreason').decode('utf-8')
            shortshotreason=json.loads(shortshotreason)
            keys=list(shortshotreason.keys())
            for i in keys:
                if float(shortshotreason[i])>0.6:
                    shortshotreason_todb.append(i)
            aoibase64=self.figdecode
            aoifigname=self.figname
        except:
            pass
        storagedata={
            "injection_speed_set":str(injection_speed_setting),
            "injection_pressure_set":str(injection_pressure_setting),
            "real_injection_speed":str(clean_injection_speed),
            "real_injection_pressure":str(clean_injection_pressure),
            "holding_pressure":str(holdingset),
            "vp":str(VP_postion),
            "vp_pressure":str(vp_pressure),
            "clamping_force":str(clamping_force),
            "holding_time":str(holding_time_setting),
            "barrel_temperature":str(barrel_temperature_setting),
            "injection_position":str(injection_postion_setting),
            "max_injection_pressure":str(maxinjectionpressure),
            "injection_end_position":str(End),
            "max_holding_pressure":str(max_holding_pressure),
            "filling_time":str(fillingtime),
            "store_postion":str(store_Postion),
            "back_postion":str(back_postion),
            "cooling_time":str(coolingtime),
            "back_pressure":str(backpressure),
            "fillingtimelimt":str(fillingtimelimt),
            "maxinjectionspeed":str(maxinjectionspeed),
            "bpnn_shortshot_prediction":str(BPNN_shortshot_predict),
            "aoibase64":str(aoibase64),
            "aoifigname":str(aoifigname),
            "shortshot_reason":str(shortshotreason_todb),
            "weight":str(weight),
            "fillingratio":str(fillingratio)
        }
        async with aiohttp.ClientSession() as session:
                try:
                    url = "http://127.0.0.1:8001/injectionmachine/history/storedata"
                    async with session.post(url,json = storagedata, timeout = 20) as response:
                        responseData = await response.json()
                        if responseData["status"] != "success":
                            print('succes save data to db....')
                except:
                    print('Fail tp save data to db....')
        # Session = sessionmaker(bind=engine)
        # session = Session()
        # tt=datetime.datetime.now()
        # insert_sql=injection_machine_DB.__table__.insert().values(
        #     injection_speed_set=str(injection_speed_setting),
        #     injection_pressure_set=str(injection_pressure_setting),
        #     real_injection_speed=str(clean_injection_speed),
        #     real_injection_pressure=str(clean_injection_pressure),
        #     holding_pressure=str(holdingset),
        #     vp=str(VP_postion),
        #     vp_pressure=str(vp_pressure),
        #     clamping_force=str(clamping_force),
        #     holding_time=str(holding_time_setting),
        #     barrel_temperature=str(barrel_temperature_setting),
        #     injection_position=str(injection_postion_setting),
        #     max_injection_pressure=str(maxinjectionpressure),
        #     injection_end_position=str(End),
        #     max_holding_pressure=str(max_holding_pressure),
        #     filling_time=str(fillingtime),
        #     ij_date=datetime.datetime.now(),
        #     store_postion=str(store_Postion),
        #     back_postion=str(back_postion),
        #     cooling_time=str(coolingtime),
        #     back_pressure=str(backpressure),
        #     fillingtimelimt=str(fillingtimelimt),
        #     maxinjectionspeed=str(maxinjectionspeed),
        #     bpnn_shortshot_prediction=str(BPNN_shortshot_predict),
        #     aoibase64=str(aoibase64),
        #     aoifigname=str(aoifigname),
        #     shortshot_reason=str(shortshotreason_todb),
        #     weight=str(weight)
        # )
        # session.execute(insert_sql)
        # session.commit()
        # session.close()
        # print('succes save data to db....')
    def predict(self):
        x=[]
        #speedset
        ijspeedset = ast.literal_eval(self.red.get('injection_speed_setting').decode('utf-8'))
        for sp in ijspeedset:
            x.append(sp)
        #real ijspeed
        realijspeed=self.red.lrange('realspeed', 0, -1)
        cleanrlijspeed=[]
        for item in realijspeed:
            cleanrlijspeed.append(float(item.decode('utf-8')))
        cleanrlijspeed_size=len(cleanrlijspeed) // 3
        realijspeed1=cleanrlijspeed[:cleanrlijspeed_size]
        realijspeed2=cleanrlijspeed[cleanrlijspeed_size:cleanrlijspeed_size*2]
        realijspeed3=cleanrlijspeed[cleanrlijspeed_size*2:]
        x.append(np.max(realijspeed1))
        x.append(np.min(realijspeed1))
        x.append(np.max(realijspeed2))
        x.append(np.min(realijspeed2))
        x.append(np.max(realijspeed3))
        x.append(np.min(realijspeed3))
        #real ijpressure
        realijpressure=self.red.lrange('realpressure', 0, -1)
        cleanrlijpressure=[]
        for item in realijpressure:
            cleanrlijpressure.append(float(item.decode('utf-8')))
        cleanrlijpressure_size=len(cleanrlijpressure) // 3
        cleanrlijpressure1=cleanrlijpressure[:cleanrlijpressure_size]
        cleanrlijpressure2=cleanrlijpressure[cleanrlijpressure_size:cleanrlijpressure_size*2]
        cleanrlijpressure3=cleanrlijpressure[cleanrlijpressure_size*2:]
        x.append(np.max(cleanrlijpressure1))
        x.append(np.min(cleanrlijpressure1))
        x.append(np.max(cleanrlijpressure2))
        x.append(np.min(cleanrlijpressure2))
        x.append(np.max(cleanrlijpressure3))
        x.append(np.min(cleanrlijpressure3))
        #  Holding pressure & holding time
        holdingpressure_setting=self.red.get('holdingset').decode('utf-8')
        holdingpressure_setting=holdingpressure_setting[1:-1].split(",")
        x.append(float(holdingpressure_setting[0]))
        x.append(float(holdingpressure_setting[1]))
        holdingtimesetting=self.red.get('holding_time_setting').decode('utf-8')
        holdingtimesetting=holdingtimesetting[1:-1].split(',')
        x.append(float(holdingtimesetting[0]))
        x.append(float(holdingtimesetting[1]))
        #dose 實際充填量
        injection_end_postion=float(self.red.get('End').decode('utf-8'))
        injection_postion=self.red.get('injection_postion_setting').decode('utf-8')[1:-1].split(",")
        injection_postion1=float(injection_postion[0])
        x.append(injection_postion1-injection_end_postion)
        #背壓
        backpressure=ast.literal_eval(self.red.get('backpressure').decode('utf-8'))
        x.append(backpressure[0])
        #injection pressure set
        x.append(float(self.red.get('injection_pressure_setting').decode('utf-8')))
        #injection postion
        x.append(float(injection_postion[0])-float(injection_postion[-1]))
        #filling time limit
        x.append(float(self.red.get('fillingtimelimt').decode('utf-8')))
        # normalize
        inputdata=[x]
        inputdata=self.normalize.transform(inputdata)
        pred=self.model.predict(inputdata)[0][0]
        predict=''
        if pred>0.5:
            predict='shortshot'
        else:
            predict='normal'
        return predict         
    def short_shot_analyis(self):
        ijpostion=self.red.get('injection_postion_setting').decode('utf-8')[1:-1].split(',')
        ijpostion_clean=[]
        ijpostion_clean2=[]
        for i in ijpostion:
            ijpostion_clean.append(i)
            ijpostion_clean2.append(float(i))
        fillingtimelimit=float(self.red.get('fillingtimelimt').decode('utf-8'))
        fillingtime=float(self.red.get('fillingtime').decode('utf-8'))
        end=float(self.red.get('End').decode('utf-8'))
        # barrel_temperature_setting=self.red.get('barrel_temperature_setting').decode('utf-8')[1:-1].split(',')
        barrel_temperature_setting=self.red.get('barrel_temperature_setting').decode('utf-8')
        #料溫
        barrel_temperature_setting_clean=[]
        # for i in barrel_temperature_setting:
        #     barrel_temperature_setting_clean.append(float(i))
        # back_pressure=self.red.get('backpressure').decode('utf-8')[1:-1].split(',')
        back_pressure=self.red.get('backpressure').decode('utf-8')
        # back_pressure_clean=[]
        # for i in back_pressure:
        #     back_pressure_clean.append(float(i))
        maxijpressure=float(self.red.get('maxinjectionpressure').decode('utf-8'))
        ijpressureset=float(self.red.get('injection_pressure_setting').decode('utf-8'))
        injection_speed_setting=self.red.get('injection_speed_setting').decode('utf-8')[1:-1].split(',')
        injection_speed_setting_clean=[]
        for i in injection_speed_setting:
            injection_speed_setting_clean.append(float(i))
        realijspeed=self.red.lrange('realspeed', 0, -1)
        cleanrlijspeed=[]
        for item in realijspeed:
            cleanrlijspeed.append(float(item.decode('utf-8')))
        evidences={
            "射出行程/自動轉保時間":dataprocess_function.compare_injectiondose_fltlimit(ijpostion_clean,fillingtimelimit)[0],
            "充填時間vs自動轉保時間":dataprocess_function.compare_flt_limit(fillingtime,fillingtimelimit)[0],
            "射出終點VS射出位置":dataprocess_function.compare_ijpos_ijend(ijpostion_clean,end)[0],
            "料管溫度VS塑料建議溫度":dataprocess_function.settingmaterialtmp_vs_materialtmpsuggestion(barrel_temperature_setting,[180,260]),
            "模溫設置VS塑料建議模溫":dataprocess_function.settingmoldtemp_vs_moldtempsuggestion(60,[40,80]),
            "當前背壓vs材料建議背壓":dataprocess_function.check_backpressure(back_pressure,[5,10]),
            "最大射壓VS射壓設定值":dataprocess_function.max_injection_pressure_compare_injection_pressure_setting(ijpressureset,maxijpressure)[0],
            "射壓設定值VS機台射壓最大值":dataprocess_function.settingpressure_vs_machinelimit(ijpressureset,1400)[0],
            "射速設定值VS機台射速最大值":dataprocess_function.settingspeed_vs_machinelimit(injection_speed_setting,200)[0],
            "實際最高射速vs射速設定最大值":dataprocess_function.compare_realinjection_ijspeedset(cleanrlijspeed,injection_speed_setting)[0],
            "最高射速行程占比":dataprocess_function.compare_max_ijspeed_postion(injection_speed_setting_clean,ijpostion_clean2)[0],
            "短射":1,            
        }
        var=["自動轉保時間時間過短","射速過低","射壓過低","計量不足","背壓過低"]
        short_shot_infer=VariableElimination(self.Bayesmodel)
        q=short_shot_infer.query(variables=var,evidence=evidences,joint =False,)
        ans={}
        for v in var:
            ans[v]=q[v].values[1]
        ans['自動轉保時間過短']=ans.pop('自動轉保時間時間過短')
        shortshotreason=json.dumps(ans)
        self.red.set('shortshotreason',shortshotreason)
        return ans  
    
    def shortshotresolution(self,shortshotcasue,fillingratio):
        AdjustmentRange=2-fillingratio
        if shortshotcasue["自動轉保時間過短"] >0.6:
            fillingtimelimt=self.client.read_variable('ST_IN_HMI')#自動轉保時間
            parameterset=fillingtimelimt*AdjustmentRange
            parameterset=parameterset//1 +1
            self.client.write_variable('ST_IN_HMI',parameterset)
        if shortshotcasue["射速過低"] >0.6:
            injection_speed_setting=self.client.read_variable('FD_IN_HMI')#射速設定值
            for i in range(len(injection_speed_setting[:5])):
                segspeed=int(injection_speed_setting[i])
                segspeed=segspeed*AdjustmentRange
                segspeed=segspeed//1 +1
                injection_speed_setting[i]=str(segspeed)
            self.client.write_variable('FD_IN_HMI',injection_speed_setting)
        if shortshotcasue["射壓過低"] >0.6:
            injection_pressure_setting=self.client.read_variable('PD_IN_HMI')
            setting=int(injection_pressure_setting[0])
            setting=setting*AdjustmentRange
            setting=setting//1 +1
            if setting > 1400:
                setting=1400
            injection_pressure_setting[0]=setting
            self.client.write_variable('PD_IN_HMI',injection_pressure_setting)
        if shortshotcasue["劑量不足"] >0.6:
            injection_postion=self.client.read_variable('SP_IN_HMI')#射出位置
            storepostion=self.client.read_variable('SP_ME_HMI')#儲料位置
            injection_postion[:5]=input['injection_postion_input']
            currentdose=injection_postion[0]-injection_postion[4]
            newdose=currentdose*AdjustmentRange
            storepostion1=0
            storepostion2=0
            if injection_postion[4] < newdose*0.1:
                injection_postion[0]=injection_postion[0]+newdose*0.1
                injection_postion[0]=math.ceil(injection_postion[0] * 10) / 10
            doseseg=newdose/4
            injection_postion[1]=injection_postion[0]-doseseg
            injection_postion[1]=math.ceil(injection_postion[1] * 10) / 10
            injection_postion[2]=injection_postion[0]-doseseg*2
            injection_postion[2]=math.ceil(injection_postion[2] * 10) / 10
            injection_postion[3]=injection_postion[0]-doseseg*3
            injection_postion[3]=math.ceil(injection_postion[3] * 10) / 10
            injection_postion[4]=injection_postion[0]-doseseg*4
            injection_postion[4]=math.ceil(injection_postion[4] * 10) / 10
            storepostion1=injection_postion[0]
            storepostion2=storepostion1+3
            storepostion[0]=storepostion1
            storepostion[1]=storepostion2
            self.client.write_variable('SP_ME_HMI',storepostion)
            self.client.write_variable('SP_IN_HMI',injection_postion)
        if shortshotcasue["背壓過低"] >0.6:
            backpressure=self.client.read_variable('SP_ME_HMI')#背壓
            backpressuresetting=backpressure[2:4]
            newbackpressuresetting=backpressuresetting[0]*AdjustmentRange
            newbackpressuresetting=newbackpressuresetting//1 +1
            backpressure[2:4]=[newbackpressuresetting,newbackpressuresetting]
            self.client.write_variable('SP_ME_HMI',backpressure)
        self.red.set('previousfillingratio',str(fillingratio))

if __name__ == '__main__':
    aoimodel=tf.keras.models.load_model("aoimodel.h5")
    processline_agent=Process_line_agent(aoimodel=aoimodel)
    processline_agent.connect()

    agent=injection_machine_class(ip='192.168.250.3')
    agent.connect()
    # processlinereset(agent.weightmeter)
    # _,_= processlinemove('normal')
    start=1
    while start==1:
        agent.collect_data()
    # classfication('c')




    # processline_agent.write_batchregister(3,118,0)
    # processline_agent.write_singleregister(3,125,32)
    # processline_agent.write_singleregister(3,125,16)
    # processline_agent.write_batchregister(4,118,0)
    # processline_agent.write_singleregister(4,125,32)
    # processline_agent.write_singleregister(4,125,16)
    # time.sleep(5)
    # processline_agent.write_batchregister(3,118,2)
    # processline_agent.write_singleregister(3,125,32)
    # processline_agent.write_singleregister(3,125,8)
    # time.sleep(5)
    # processline_agent.write_batchregister(3,118,3)
    # processline_agent.write_singleregister(3,125,32)
    # processline_agent.write_singleregister(3,125,8)
    # time.sleep(5)
    # processline_agent.write_batchregister(3,118,4)
    # processline_agent.write_singleregister(3,125,32)
    # processline_agent.write_singleregister(3,125,8)
        
    # processlinemove("normal")


            



            

