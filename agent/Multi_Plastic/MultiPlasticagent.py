from aphyt import omron
import pika
import redis
import numpy as np
from datetime import datetime,timezone
import os
import json
from sqlalchemy import create_engine,text, Column, Integer, String,DateTime,TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
import base64
import math
import time
Base = declarative_base()
class injection_machine_db(Base):
    __tablename__    = "MachineHistory"
    id               = Column(Integer, primary_key=True)
    created_at       = Column(TIMESTAMP)
    machine_name     = Column(TEXT)
    machine_status   = Column(TEXT)
    machine_feedback = Column(TEXT)
    machine_curve    = Column(TEXT)

class multiplasticagent:
    def __init__(self,machineaddress,machineid):
        self.rabbitmq_account  = "cax"
        self.rabbitmq_password = "cax521"
        self.hostip            = "192.168.1.50"
        self.machineid         = machineid
        self.machineaddress    = machineaddress
        self.processactivate   = False
        self.worker            = ""
        self.red = redis.Redis(host='192.168.1.50',port=6379,db=0)
        self.actpressurecurve = []
        self.actspeedcurve    = []
        self.motorpower       = []
        self.heaterpower      = []
        self.screwposition    = []
        self.timeindex        = []
        self.machinestatus    = {}
        self.machinefeedback  = {}
        self.machinecurve     = {}
        self.db = create_engine("postgresql://postgres:postgres@192.168.1.50:5432/cax")
        self.nodemap = {
            "injection_pressure1_set":{'id':"PD_IN_HMI",'index':0},
            "barrel_temp1_set":{'id':"S_TE_HMI",'index':0},
            "barrel_temp2_set":{'id':"S_TE_HMI",'index':1},
            "barrel_temp3_set":{'id':"S_TE_HMI",'index':2},
            "barrel_temp4_set":{'id':"S_TE_HMI",'index':3},
            "barrel_temp5_set":{'id':"S_TE_HMI",'index':4},
            "injection_volume1":{'id':"SP_IN_HMI",'index':0},
            "injection_volume2":{'id':"SP_IN_HMI",'index':1},
            "injection_volume3":{'id':"SP_IN_HMI",'index':2},
            "injection_volume4":{'id':"SP_IN_HMI",'index':3},
            "injection_volume5":{'id':"SP_IN_HMI",'index':4},
            "injection_rate1_set":{'id':"FD_IN_HMI",'index':0},
            "injection_rate2_set":{'id':"FD_IN_HMI",'index':1},
            "injection_rate3_set":{'id':"FD_IN_HMI",'index':2},
            "injection_rate4_set":{'id':"FD_IN_HMI",'index':3},
            "injection_rate5_set":{'id':"FD_IN_HMI",'index':4},
            "clamp_force_set":{'id':"FD_MC_HMI",'index':4},
            "filling_time_set":{'id':"ST_IN_HMI",'index':0},
            "backpressure1":{'id':"PD_ME_HMI",'index':2},
            "backpressure2":{'id':"PD_ME_HMI",'index':3},
            "holding_time1_set":{'id':"ST_HD_HMI",'index':0},
            "holding_time2_set":{'id':"ST_HD_HMI",'index':1},
            "holding_time3_set":{'id':"ST_HD_HMI",'index':2},
            "holding_pressure1_set":{'id':"PD_HD_HMI",'index':0},
            "holding_pressure2_set":{'id':"PD_HD_HMI",'index':1},
            "holding_pressure3_set":{'id':"PD_HD_HMI",'index':2},
            "cooling_time":{'id':"ST_HD_HMI",'index':6},
            "vp_position_set":{'id':"D_SPC_SAVE",'index':1},
            "dos_position1":{'id':"SP_ME_HMI",'index':0},
            "dos_position2":{'id':"SP_ME_HMI",'index':1},
        }
        
    def connect(self):  
        self.worker=omron.n_series.NSeries()
        try:
            self.worker.connect_explicit(self.machineaddress)
            self.worker.register_session()
            self.worker.update_variable_dictionary()
            print("[MESSAGE] Success connect")
            def callback(ch, method, properties, body):
                command = json.loads(body.decode())
                self.parametersetting(command["Target"],command["Value"])
            def start_controller():
                while True:
                    try:
                        connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=self.hostip,
                            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_password)
                        ))
                        channel = connection.channel()
                        channel.queue_declare(queue=self.machineid)
                        channel.basic_consume(queue=self.machineid,
                                on_message_callback=callback,
                                auto_ack=True)
                        channel.start_consuming()
                    except Exception as e:
                        print(e)
                        time.sleep(5)
            controller_thread = threading.Thread(target=start_controller)
            controller_thread.start()
            print("[MESSAGE] Activate Rabbit MQ ..")
        except Exception as e:
            print(e)
            print("[ERROR] Connect to Engel fail")
    
    def parametersetting(self,target,value):
        access_node = list(self.nodemap.keys())
        if target in access_node:
            nodeid = self.nodemap[target]['id']
            index  = self.nodemap[target]['index']
            value  = float(value)
            originvalue = self.worker.read_variable(nodeid)
            newvalue = originvalue
            newvalue[index] = value
            self.worker.write_variable(nodeid,newvalue)

            
    def collectdata(self):
        # Mold close singal
        moldclose=self.worker.read_variable('Y23B')
        respeed=self.worker.read_variable('D_MA_HMI')[6]#當前射出速度
        respeed=math.floor(respeed * 100)/100.0
        # Injection pressure setting
        injection_pressure_list                            = {}
        injection_pressure1_set                            = self.worker.read_variable('PD_IN_HMI')[0]
        injection_pressure_list["injection_pressure1_set"] = {"value":injection_pressure1_set,"edit":"none"}
        self.machinestatus["injection_pressure_list"]      = injection_pressure_list
        # Barrel Temp set
        barrel_temperature_setting=self.worker.read_variable('S_TE_HMI')[:5]
        barrel_temp_set = {}
        barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temperature_setting[0],"edit":"none"}
        barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temperature_setting[1],"edit":"none"}
        barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temperature_setting[2],"edit":"none"}
        barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temperature_setting[3],"edit":"none"}
        barrel_temp_set["barrel_temp5_set"]   = {"value":barrel_temperature_setting[4],"edit":"none"}
        self.machinestatus["barrel_temp_set"] = barrel_temp_set
        
        # Injection position 
        injection_postion_setting=self.worker.read_variable('SP_IN_HMI')[:5]
        injection_postion_setting=[math.floor(a * 100)/100.0 for a in injection_postion_setting]
        injection_pos ={}
        injection_pos["injection_volume1"]     = {"value":injection_postion_setting[0],"edit":"none"}
        injection_pos["injection_volume2"]     = {"value":injection_postion_setting[1],"edit":"none"}
        injection_pos["injection_volume3"]     = {"value":injection_postion_setting[2],"edit":"none"}
        injection_pos["injection_volume4"]     = {"value":injection_postion_setting[3],"edit":"none"}
        injection_pos["injection_volume5"]     = {"value":injection_postion_setting[4],"edit":"none"}
        self.machinestatus["injection_pos"]    = injection_pos
        # Injection Speed
        injection_speed = {}
        injection_speed_setting=self.worker.read_variable('FD_IN_HMI')[:5]
        injection_speed_setting=[math.floor(a * 100)/100.0 for a in injection_speed_setting] 
        injection_speed["injection_rate1_set"]   = {"value":injection_speed_setting[0],"edit":"none"}
        injection_speed["injection_rate2_set"]   = {"value":injection_speed_setting[1],"edit":"none"}
        injection_speed["injection_rate3_set"]   = {"value":injection_speed_setting[2],"edit":"none"}
        injection_speed["injection_rate4_set"]   = {"value":injection_speed_setting[3],"edit":"none"}
        injection_speed["injection_rate5_set"]   = {"value":injection_speed_setting[4],"edit":"none"}
        self.machinestatus["injection_speed"]    = injection_speed
        #Clamp force set
        clamp_force_set                        = self.worker.read_variable('FD_MC_HMI')[4]
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"none"}
        #Filling Time Limit Setting
        filling_time_limit_set                       = self.worker.read_variable('ST_IN_HMI')[0]
        self.machinestatus["filling_time_set"] = {"value":filling_time_limit_set,"edit":"none"}
        #Back pressure
        backpressure  = {}
        ackpressure=self.worker.read_variable('PD_ME_HMI')[2:4]
        backpressure["backpressure1"]       = {"value":ackpressure[0],"edit":"none"}
        backpressure["backpressure2"]       = {"value":ackpressure[1],"edit":"none"}
        self.machinestatus["backpressure"]  = backpressure
        #Holding time setting
        holdingtimeset = {}
        holding_time_setting=self.worker.read_variable('ST_HD_HMI')[:3]
        holding_time_setting=[math.floor(a * 100)/100.0 for a in holding_time_setting]
        holdingtimeset["holding_time1_set"]     = {"value":holding_time_setting[0],"edit":"none"}
        holdingtimeset["holding_time2_set"]     = {"value":holding_time_setting[1],"edit":"none"}
        holdingtimeset["holding_time3_set"]     = {"value":holding_time_setting[2],"edit":"none"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset
        # Holding pressure
        holdingpressureset ={}
        holdingset=self.worker.read_variable('PD_HD_HMI')[:3]
        holdingpressureset["holding_pressure1_set"] = {"value":holdingset[0],"edit":"none"}
        holdingpressureset["holding_pressure2_set"] = {"value":holdingset[1],"edit":"none"}
        holdingpressureset["holding_pressure3_set"] = {"value":holdingset[2],"edit":"none"}
        self.machinestatus["holdingpressureset"]    = holdingpressureset
        #Cooling time
        cooling_time                          = self.worker.read_variable('ST_HD_HMI')[6]
        cooling_time=math.floor(cooling_time * 100)/100.0
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"none"}
        #VP position setting
        vp_position_set                       = self.worker.read_variable('D_SPC_SAVE')[1]
        self.machinestatus["vp_position_set"] = {"value":vp_position_set,"edit":"none"}
        # Dos Position
        Dospos = {}
        store_postion=self.worker.read_variable('SP_ME_HMI')[:2]
        Dospos["dos_position1"]       = {"value":store_postion[0],"edit":"none"}
        Dospos["dos_position2"]       = {"value":store_postion[1],"edit":"none"}
        self.machinestatus["Dospos"]  = Dospos
        # Check processstatus
        if moldclose is True and respeed !=0:
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
            # Collect act injection pressure
            repressure=self.worker.read_variable('D_MA_HMI')[18]#當前射出壓力
            repressure=math.floor(repressure * 100)/100.0
            self.actpressurecurve.append(repressure)
            # Collect act injection speed
            respeed=math.floor(respeed * 100)/100.0
            self.actspeedcurve.append(respeed)
            # Collect screw position
            screwpos=self.worker.read_variable('SVAX0_DACT')[0]#螺桿即時位置
            screwpos=math.floor(screwpos * 100)/100.0
            self.screwposition.append(screwpos)
            self.machinecurve["actpressurecurve"] = self.actpressurecurve
            self.machinecurve["actspeedcurve"]    = self.actspeedcurve
            self.machinecurve["screwposition"]    = self.screwposition
        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                # FEED BACK 
                print("[Message] Save data ...")
                # Act vp pressure
                vp_pressure=self.worker.read_variable('D_SPC_SAVE')[9]#VP轉換壓
                self.machinefeedback["Act_vp_pressure"] = vp_pressure
                # Act filling time
                actfillingtime=self.worker.read_variable('D_SPC_SAVE')[5]#充填時間
                self.machinefeedback["actfillingtime"] = actfillingtime
                # Act filling end
                End=self.worker.read_variable('D_MA_HMI')[15]#射出終點
                End=math.floor(End * 100)/100.0
                self.machinefeedback["Filling_end"] = End
                # Act Max holding pressure
                max_holding_pressure=self.worker.read_variable('SPC_PD_HD')[1]#保壓峰值
                self.machinefeedback["max_holding_pressure"] = max_holding_pressure
                self.processactivate =False
                # TYPE SAVE TO DB CODE HERE !!!!!!!!!!!!
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                Session = sessionmaker(bind=self.db)
                session = Session()
                insert_sql = injection_machine_db.__table__.insert().values(
                    created_at       = current_time,
                    machine_name     = self.machineid,
                    machine_status  = json.dumps(self.machinestatus),
                    machine_feedback = json.dumps(self.machinefeedback),
                    machine_curve    = json.dumps(self.machinecurve)
                )
                session.execute(insert_sql)
                session.commit()
                session.close()
                # DBPLAN save MachineID updatetime status(dumps(dict)) feedback(dumps(dict)) curve((dumps(dict))) ....
                #Clean act injection pressure&speed act motor power curve 
                self.actpressurecurve = []
                self.actspeedcurve    = []
                self.motorpower       = []
                self.heaterpower      = []
                self.screwposition    = []
                self.timeindex        = []
        #Get current time
        current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'{self.machineid}_updatetime',current_time)
        self.red.set(f'{self.machineid}_status',json.dumps(self.machinestatus))
        self.red.set(f'{self.machineid}_feedback',json.dumps(self.machinefeedback))
        self.red.set(f'{self.machineid}_curve',json.dumps(self.machinecurve))
if __name__ == "__main__":
    machineaddress = '192.168.250.3'
    MULTIPAS          = multiplasticagent(machineaddress,'MULTIPAS-MuCell')
    MULTIPAS.connect()
    while True:
      try:
        MULTIPAS.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




