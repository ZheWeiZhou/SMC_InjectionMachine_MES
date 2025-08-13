from opcua import Client
from opcua import ua
import pika
import redis
import numpy as np
from datetime import datetime
import os
import json
from sqlalchemy import create_engine,text, Column, Integer, String,DateTime,TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
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

class chenghsongagent:
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
            "holding_time1_set":{'nodeid':'ns=1;i=269746226','factor':100,'type':'float'},
            "holding_time2_set":{'nodeid':'ns=1;i=269746227','factor':100,'type':'float'},
            "holding_time3_set":{'nodeid':'ns=1;i=269746228','factor':100,'type':'float'},
            "holding_time4_set":{'nodeid':'ns=1;i=269746229','factor':100,'type':'float'},
            "holding_pressure1_set":{'nodeid':'ns=1;i=269746186','factor':1,'type':'float'},
            "holding_pressure2_set":{'nodeid':'ns=1;i=269746187','factor':1,'type':'float'},
            "holding_pressure3_set":{'nodeid':'ns=1;i=269746188','factor':1,'type':'float'},
            "holding_pressure4_set":{'nodeid':'ns=1;i=269746189','factor':1,'type':'float'},
            "injection_volume1":{'nodeid':'ns=1;i=269877251','factor':100,'type':'float'},
            "injection_volume2":{'nodeid':'ns=1;i=269746236','factor':100,'type':'float'},
            "injection_volume3":{'nodeid':'ns=1;i=269746237','factor':100,'type':'float'},
            "injection_volume4":{'nodeid':'ns=1;i=269746238','factor':100,'type':'float'},
            "injection_volume5":{'nodeid':'ns=1;i=269746239','factor':100,'type':'float'},
            "injection_volume6":{'nodeid':'ns=1;i=269680644','factor':100,'type':'float'},
            "injection_rate1_set":{'nodeid':'ns=1;i=269746196','factor':10,'type':'float'},
            "injection_rate2_set":{'nodeid':'ns=1;i=269746197','factor':10,'type':'float'},
            "injection_rate3_set":{'nodeid':'ns=1;i=269746198','factor':10,'type':'float'},
            "injection_rate4_set":{'nodeid':'ns=1;i=269746199','factor':10,'type':'float'},
            "injection_rate5_set":{'nodeid':'ns=1;i=269746200','factor':10,'type':'float'},
            "injection_pressure1_set":{'nodeid':'ns=1;i=269746176','factor':1,'type':'float'},
            "injection_pressure2_set":{'nodeid':'ns=1;i=269746177','factor':1,'type':'float'},
            "injection_pressure3_set":{'nodeid':'ns=1;i=269746178','factor':1,'type':'float'},
            "injection_pressure4_set":{'nodeid':'ns=1;i=269746179','factor':1,'type':'float'},
            "injection_pressure5_set":{'nodeid':'ns=1;i=269746180','factor':1,'type':'float'},
            "backpressure1":{'nodeid':'ns=1;i=269746246','factor':1,'type':'float'},
            "backpressure2":{'nodeid':'ns=1;i=269746247','factor':1,'type':'float'},
            "backpressure3":{'nodeid':'ns=1;i=269746248','factor':1,'type':'float'},
            "cooling_time":{'nodeid':'ns=1;i=286457857','factor':100,'type':'float'},
            "clamp_force_set":{'nodeid':'ns=1;i=605159442','factor':1,'type':'float'},
            "filling_time_set":{'nodeid':'ns=1;i=269680646','factor':100,'type':'float'},
        }
        
    def connect(self):  
        url="opc.tcp://"+self.machineaddress
        self.worker=Client(url)
        try:
            self.worker.connect()
            print("[MESSAGE] Success connect to Engel")
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
            nodeid = self.nodemap[target]['nodeid']
            factor = self.nodemap[target]['factor']
            value  = float(value)*factor
            int32value = int(value)
            self.worker.get_node(nodeid).set_value(ua.Variant(int32value, ua.VariantType.Int32))

    def productpredict(self,input):
        print("[MESSAGE] Start to predict product quality")
        modelinput=np.array([input])
        print(modelinput)
        normodelinput=self.normalize.transform(modelinput)
        print(f'Nor {normodelinput}')
        modelresponse=self.model.predict(normodelinput)[0]
        print(f"Model response{modelresponse}")
        if modelresponse >0.5:
            modelresponse=1
            ProductQ="ng"
        else:
            modelresponse=0
            ProductQ="good"
        self.red.set('ProductQ',ProductQ)
        self.red.set('nglevel',str(modelresponse))
        print(f'[Message] model predict response: {modelresponse}')
    def collectdata(self):
        # Check processstatus
        processstatus                      = self.worker.get_node("ns=1;i=269877271").get_value()
        # barrel temp
        barrel_temp_set = {}
        barrel_temp1_set                      = self.worker.get_node("ns=1;i=85131264").get_value()
        barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temp1_set,"edit":"none"}
        barrel_temp2_set                      = self.worker.get_node("ns=1;i=85131265").get_value()
        barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temp2_set,"edit":"none"}
        barrel_temp3_set                      = self.worker.get_node("ns=1;i=85131266").get_value()
        barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temp3_set,"edit":"none"}
        barrel_temp4_set                      = self.worker.get_node("ns=1;i=85131267").get_value()
        barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temp4_set,"edit":"none"}
        barrel_temp5_set                      = self.worker.get_node("ns=1;i=85131268").get_value()
        barrel_temp_set["barrel_temp5_set"]   = {"value":barrel_temp5_set,"edit":"none"}
        barrel_temp6_set                      = self.worker.get_node("ns=1;i=85131269").get_value()
        barrel_temp_set["barrel_temp6_set"]   = {"value":barrel_temp6_set,"edit":"none"}
        barrel_temp7_set                      = self.worker.get_node("ns=1;i=85131270").get_value()
        barrel_temp_set["barrel_temp7_set"]   = {"value":barrel_temp7_set,"edit":"none"}
        self.machinestatus["barrel_temp_set"] = barrel_temp_set

        barrel_temp_real = {}
        barrel_temp1_real                      = self.worker.get_node("ns=1;i=85327875").get_value()
        barrel_temp_real["barrel_temp1_real"]  = {"value":barrel_temp1_real,"edit":"none"}
        barrel_temp2_real                      = self.worker.get_node("ns=1;i=85327876").get_value()
        barrel_temp_real["barrel_temp2_real"]  = {"value":barrel_temp2_real,"edit":"none"}
        barrel_temp3_real                      = self.worker.get_node("ns=1;i=85327877").get_value()
        barrel_temp_real["barrel_temp3_real"]  = {"value":barrel_temp3_real,"edit":"none"}
        barrel_temp4_real                      = self.worker.get_node("ns=1;i=85327878").get_value()
        barrel_temp_real["barrel_temp4_real"]  = {"value":barrel_temp4_real,"edit":"none"}
        barrel_temp5_real                      = self.worker.get_node("ns=1;i=85327879").get_value()
        barrel_temp_real["barrel_temp5_real"]  = {"value":barrel_temp5_real,"edit":"none"}
        barrel_temp6_real                      = self.worker.get_node("ns=1;i=85327880").get_value()
        barrel_temp_real["barrel_temp6_real"]  = {"value":barrel_temp6_real,"edit":"none"}
        barrel_temp7_real                      = self.worker.get_node("ns=1;i=85327881").get_value()
        barrel_temp_real["barrel_temp7_real"]  = {"value":barrel_temp7_real,"edit":"none"}
        self.machinestatus["barrel_temp_real"] = barrel_temp_real

        #Holding pressure & time setting
        holdingtimeset = {}
        holding_time1_set                       = self.worker.get_node("ns=1;i=269746226").get_value()/100
        holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"acctivate"}
        holding_time2_set                       = self.worker.get_node("ns=1;i=269746227").get_value()/100
        holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"acctivate"}
        holding_time3_set                       = self.worker.get_node("ns=1;i=269746228").get_value()/100
        holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"acctivate"}
        holding_time4_set                       = self.worker.get_node("ns=1;i=269746229").get_value()/100
        holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"acctivate"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset

        holdingpressureset ={}
        holding_pressure1_set                       = self.worker.get_node("ns=1;i=269746186").get_value()
        holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"acctivate"}
        holding_pressure2_set                       = self.worker.get_node("ns=1;i=269746187").get_value()
        holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"acctivate"}
        holding_pressure3_set                       = self.worker.get_node("ns=1;i=269746188").get_value()
        holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"acctivate"}
        holding_pressure4_set                       = self.worker.get_node("ns=1;i=269746189").get_value()
        holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"acctivate"}
        self.machinestatus["holdingpressureset"]    = holdingpressureset
        #Injection volume(position) set
        injectionseg                           = self.worker.get_node("ns=1;i=269680647").get_value()
        injection_pos ={}
        injection_volume1                      = self.worker.get_node("ns=1;i=269877251").get_value()/100
        injection_pos["injection_volume1"]     = {"value":injection_volume1,"edit":"acctivate"}
        injection_volume2                      = -1 if injectionseg < 3 else self.worker.get_node("ns=1;i=269746236").get_value()/100
        injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"acctivate"}
        injection_volume3                      = -1 if injectionseg < 4 else self.worker.get_node("ns=1;i=269746237").get_value()/100
        injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"acctivate"}
        injection_volume4                      = -1 if injectionseg < 5 else self.worker.get_node("ns=1;i=269746238").get_value()/100
        injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"acctivate"}
        injection_volume5                      = -1 if injectionseg < 6 else self.worker.get_node("ns=1;i=269746239").get_value()/100
        injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"acctivate"}
        #  injection_volume6  = vp position set on HMI
        injection_volume6                      = self.worker.get_node("ns=1;i=269680644").get_value()/100
        injection_pos["injection_volume6"]     = {"value":injection_volume6,"edit":"acctivate"}
        self.machinestatus["injection_pos"]    = injection_pos
        #Injection rate(speed) set
        injection_speed = {}
        injection_rate1_set                      = self.worker.get_node("ns=1;i=269746196").get_value()/10
        injection_speed["injection_rate1_set"]   = {"value":injection_rate1_set,"edit":"acctivate"}
        injection_rate2_set                      = -1 if injectionseg < 2 else self.worker.get_node("ns=1;i=269746197").get_value()/10
        injection_speed["injection_rate2_set"]   = {"value":injection_rate2_set,"edit":"acctivate"}
        injection_rate3_set                      = -1 if injectionseg < 3 else self.worker.get_node("ns=1;i=269746198").get_value()/10
        injection_speed["injection_rate3_set"]   = {"value":injection_rate3_set,"edit":"acctivate"}
        injection_rate4_set                      = -1 if injectionseg < 4 else self.worker.get_node("ns=1;i=269746199").get_value()/10
        injection_speed["injection_rate4_set"]   = {"value":injection_rate4_set,"edit":"acctivate"}
        injection_rate5_set                      = -1 if injectionseg < 5 else self.worker.get_node("ns=1;i=269746200").get_value()/10 
        injection_speed["injection_rate5_set"]   = {"value":injection_rate5_set,"edit":"acctivate"} 
        self.machinestatus["injection_speed"]    = injection_speed
        #Cooling time
        cooling_time                          = self.worker.get_node("ns=1;i=286457857").get_value()/100
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"acctivate"}
        #Injection pressure setting
        injection_pressure_list                            = {}
        injection_pressure1_set                            = self.worker.get_node("ns=1;i=269746176").get_value()
        injection_pressure_list["injection_pressure1_set"] = {"value":injection_pressure1_set,"edit":"acctivate"}
        injection_pressure2_set                            = -1 if injectionseg < 2 else self.worker.get_node("ns=1;i=269746177").get_value()
        injection_pressure_list["injection_pressure2_set"] = {"value":injection_pressure2_set,"edit":"acctivate"}
        injection_pressure3_set                            = -1 if injectionseg < 3 else self.worker.get_node("ns=1;i=269746178").get_value()
        injection_pressure_list["injection_pressure3_set"] = {"value":injection_pressure3_set,"edit":"acctivate"}
        injection_pressure4_set                            = -1 if injectionseg < 4 else self.worker.get_node("ns=1;i=269746179").get_value()
        injection_pressure_list["injection_pressure4_set"] = {"value":injection_pressure4_set,"edit":"acctivate"}
        injection_pressure5_set                            = -1 if injectionseg < 5 else  self.worker.get_node("ns=1;i=269746180").get_value()
        injection_pressure_list["injection_pressure5_set"] = {"value":injection_pressure5_set,"edit":"acctivate"}
        self.machinestatus["injection_pressure_list"]      = injection_pressure_list
        #Back pressure
        backpressureseg = self.worker.get_node("ns=1;i=269680648").get_value() 
        backpressure    = {}
        backpressure1                       = self.worker.get_node("ns=1;i=269746246").get_value()
        backpressure["backpressure1"]       = {"value":backpressure1,"edit":"acctivate"}
        backpressure2                       = -1 if backpressureseg < 2 else self.worker.get_node("ns=1;i=269746247").get_value()
        backpressure["backpressure2"]       = {"value":backpressure2,"edit":"acctivate"}
        backpressure3                       = -1 if backpressureseg < 3 else self.worker.get_node("ns=1;i=269746248").get_value()
        backpressure["backpressure3"]       = {"value":backpressure3,"edit":"acctivate"}
        self.machinestatus["backpressure"]  = backpressure
        #Clamp force set
        clamp_force_set                        = self.worker.get_node("ns=1;i=605159442").get_value()
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"acctivate"}
        # Filling Time
        filling_time_set = self.worker.get_node("ns=1;i=269680646").get_value()/100
        self.machinestatus["filling_time_set"]    = {"value":filling_time_set,"edit":"acctivate"}
        if processstatus != 65026 and processstatus != 0 :
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
            # #Collect Realtime IJ presure
            actijpressure = self.worker.get_node("ns=1;i=118882368").get_value()
            self.actpressurecurve.append(actijpressure)

            self.machinecurve["actpressurecurve"] = self.actpressurecurve

        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                print("[Message] Save data ...")
                # Material Cushion (餘料)
                material_cushion                         = self.worker.get_node("ns=1;i=269877252").get_value()
                self.machinefeedback["material_cushion"] = material_cushion
                #Filling time
                filling_time                         = self.worker.get_node("ns=1;i=269877250").get_value()
                self.machinefeedback["filling_time"] = filling_time
                #Maximun real injection pressure
                Maximun_real_injection_pressure                         = self.worker.get_node("ns=1;i=269877268").get_value()
                self.machinefeedback["Maximun_real_injection_pressure"] = Maximun_real_injection_pressure
                #Maximun real injection speed
                maximun_real_injection_speed                         = self.worker.get_node("ns=1;i=269877324").get_value()/10
                self.machinefeedback["maximun_real_injection_speed"] = maximun_real_injection_speed
                #VP position real
                vp_position_real                         = self.worker.get_node("ns=1;i=269877253").get_value()/100
                self.machinefeedback["vp_position_real"] = vp_position_real
                #real vp pressure
                real_vp_pressure                         = self.worker.get_node("ns=1;i=269877255").get_value()
                self.machinefeedback["real_vp_pressure"] = real_vp_pressure
                #real vp speed
                real_vp_speed                         = self.worker.get_node("ns=1;i=269877255").get_value()
                self.machinefeedback["real_vp_speed"] = real_vp_speed
                #Act cycle time
                act_cycle_time                         = self.worker.get_node("ns=1;i=1441832").get_value()
                self.machinefeedback["act_cycle_time"] = act_cycle_time
                #Max Holding pressure
                max_hold_pressure                         = self.worker.get_node("ns=1;i=269877269").get_value()
                self.machinefeedback["max_hold_pressure"] = max_hold_pressure

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
    machineaddress = '192.168.1.11:4840'
    chenghsong          = chenghsongagent(machineaddress,'ChenHsong')
    chenghsong.connect()
    while True:
      try:
        chenghsong.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




