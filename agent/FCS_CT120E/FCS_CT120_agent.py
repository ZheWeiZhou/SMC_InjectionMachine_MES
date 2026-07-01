from opcua import Client
from opcua import ua
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
import copy
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

class fcsagent:
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
        self.screwposition    = []
        self.machinestatus    = {}
        self.machinefeedback  = {}
        self.machinecurve     = {}
        self.db = create_engine("postgresql://postgres:postgres@192.168.1.50:5432/cax")
        self.nodemap = {
        }
        self.cycle_counter = 0
        self.has_plastic = False
        
    def connect(self):  
        url="opc.tcp://"+self.machineaddress
        self.worker=Client(url)
        try:
            self.worker.connect()
            self.cycle_counter  = self.worker.get_node("ns=2;i=21131").get_value()
            print("[MESSAGE] Success connect to Machine")
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
            datatype = self.nodemap[target]['type']
            value  = float(value)*factor
            data_value = ua.DataValue()
            if datatype == 'float':
                data_value.Value = ua.Variant(value, ua.VariantType.Float)
            elif datatype == 'int64':
                value = int(value)
                data_value.Value = ua.Variant(value, ua.VariantType.Int64)
            elif datatype == 'button':
                value = bool(int(value))
                data_value.Value = ua.Variant(value, ua.VariantType.Boolean)
                self.worker.get_node(nodeid).set_value(data_value)
                value = bool(int(0))
                data_value.Value = ua.Variant(value, ua.VariantType.Boolean)

            data_value.ServerTimestamp = None
            data_value.SourceTimestamp = None
            data_value.StatusCode = ua.StatusCode(ua.StatusCodes.Good)
            self.worker.get_node(nodeid).set_value(data_value)
            
        try:
            injection_postion= copy.deepcopy(self.machinestatus["injection_pos"])
            if "injection_volume" in target:
                injection_postion[target] = {"value":float(value)/1.5204,"edit":"none"}
            injection_pos_key= list(injection_postion.keys())
            posset = []
            for key in injection_pos_key:
                positem = injection_postion[key]["value"]
                if positem >= 0:
                    posset.append(positem)
            ijendpos = min(posset)
            print(ijendpos)
            ijendpos = ijendpos*1.5204
            vppos_value = ua.DataValue()
            vppos_value.Value = ua.Variant(ijendpos, ua.VariantType.Float)
            vppos_value.ServerTimestamp = None
            vppos_value.SourceTimestamp = None
            vppos_value.StatusCode = ua.StatusCode(ua.StatusCodes.Good)
            self.worker.get_node('ns=4;s=APPL.Injection1.sv_CutOffParams.rPositionThreshold').set_value(vppos_value)
        except Exception as e:
            print(e)


        
            
    def getmachinestatus(self):
        injection_signal = self.worker.get_node("ns=2;i=21147").get_value()
        holding_signal   = self.worker.get_node("ns=2;i=21146").get_value()
        plastic_signal   = self.worker.get_node("ns=2;i=21148").get_value()
        cycle_counter    = self.worker.get_node("ns=2;i=21131").get_value()
        moldclosing      = self.worker.get_node("ns=2;i=21159").get_value()
        if plastic_signal ==1:
            self.has_plastic = True
        if moldclosing ==1 or injection_signal==1 or holding_signal==1 or plastic_signal ==1:
            return True
        else:
            if self.processactivate == True and self.has_plastic == False:
                return True
            return False


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
        processstatus                      = self.getmachinestatus()
        # barrel temp
        barrel_temp_set = {}
        barrel_temp1_set                      = self.worker.get_node("ns=2;i=20555").get_value() / 10
        barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temp1_set,"edit":"none"}
        barrel_temp2_set                      = self.worker.get_node("ns=2;i=20544").get_value() / 10
        barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temp2_set,"edit":"none"}
        barrel_temp3_set                      = self.worker.get_node("ns=2;i=20533").get_value() / 10
        barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temp3_set,"edit":"none"}
        barrel_temp4_set                      = self.worker.get_node("ns=2;i=20522").get_value() / 10
        barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temp4_set,"edit":"none"}
        barrel_temp5_set                      = self.worker.get_node("ns=2;i=20500").get_value() / 10
        barrel_temp_set["barrel_temp5_set"]   = {"value":barrel_temp4_set,"edit":"none"}
        self.machinestatus["barrel_temp_set"] = barrel_temp_set

        barrel_temp_real = {}
        barrel_temp1_real                      = self.worker.get_node("ns=2;i=21188").get_value() / 10
        barrel_temp_real["barrel_temp1_real"]  = {"value":barrel_temp1_real,"edit":"none"}
        barrel_temp2_real                      = self.worker.get_node("ns=2;i=21187").get_value() / 10
        barrel_temp_real["barrel_temp2_real"]  = {"value":barrel_temp2_real,"edit":"none"}
        barrel_temp3_real                      = self.worker.get_node("ns=2;i=21186").get_value() / 10
        barrel_temp_real["barrel_temp3_real"]  = {"value":barrel_temp3_real,"edit":"none"}
        barrel_temp4_real                      = self.worker.get_node("ns=2;i=21185").get_value() / 10
        barrel_temp_real["barrel_temp4_real"]  = {"value":barrel_temp4_real,"edit":"none"}
        barrel_temp5_real                      = self.worker.get_node("ns=2;i=21183").get_value() / 10
        barrel_temp_real["barrel_temp5_real"]  = {"value":barrel_temp5_real,"edit":"none"}
        self.machinestatus["barrel_temp_real"] = barrel_temp_real

        holdseg = self.worker.get_node("ns=2;i=20715").get_value()
        #Holding pressure & time setting
        holdingtimeset = {}
        holding_time1_set                       = self.worker.get_node("ns=2;i=20716").get_value() / 1000
        holdingtimeset["holding_time1_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 1:
            holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"none"}
        holding_time2_set                       = self.worker.get_node("ns=2;i=20717").get_value() / 1000
        holdingtimeset["holding_time2_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 2:
            holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"none"}
        holding_time3_set                       = self.worker.get_node("ns=2;i=20718").get_value() / 1000
        holdingtimeset["holding_time3_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 3:
            holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"none"}
        holding_time4_set                       = self.worker.get_node("ns=2;i=20719").get_value() / 1000
        holdingtimeset["holding_time4_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 4:
            holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"none"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset

        holdingpressureset ={}
        holding_pressure1_set                       = self.worker.get_node("ns=2;i=20709").get_value() / 1000
        holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"none"}
        holding_pressure2_set                       = self.worker.get_node("ns=2;i=20710").get_value() /1000
        holdingpressureset["holding_pressure2_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 2:
            holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"none"}
        holding_pressure3_set                       = self.worker.get_node("ns=2;i=20711").get_value() /1000
        holdingpressureset["holding_pressure3_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 3:
            holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"none"}
        holding_pressure4_set                       = self.worker.get_node("ns=2;i=20712").get_value() /1000
        holdingpressureset["holding_pressure4_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 4:
            holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"none"}

        self.machinestatus["holdingpressureset"]    = holdingpressureset
        # Back pressure
        backpressure  = {}
        backpressure1                       = self.worker.get_node("ns=2;i=21195").get_value() / 1000
        backpressure["backpressure1"]       = {"value":backpressure1,"edit":"none"}
        self.machinestatus["backpressure"]  = backpressure
        numofseg = self.worker.get_node("ns=2;i=20740").get_value()
        # Cut of position
        vp_position_set = self.worker.get_node("ns=2;i=20753").get_value()/10000
        self.machinestatus["vp_position_set"]  = {"value":vp_position_set,"edit":"none"}    
        # Injection volume(position) set
        injection_pos ={}
        injection_volume1                      = self.worker.get_node("ns=2;i=21201").get_value()/10000
        injection_pos["injection_volume1"]     = {"value":injection_volume1,"edit":"none"}
        injection_volume2                      = self.worker.get_node("ns=2;i=20730").get_value()/10000
        injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"none"}
        injection_volume3                      = self.worker.get_node("ns=2;i=20731").get_value()/10000
        injection_pos["injection_volume3"]     = {"value":-1,"edit":"none"}
        if numofseg >=3:
            injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"none"}
        injection_volume4                      = self.worker.get_node("ns=2;i=20732").get_value()/10000
        injection_pos["injection_volume4"]     = {"value":-1,"edit":"none"}
        if numofseg >=4:
            injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"none"}
        injection_volume5                      = self.worker.get_node("ns=2;i=20733").get_value()/10000
        injection_pos["injection_volume5"]     = {"value":-1,"edit":"none"}
        if numofseg >=5:
            injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"none"}
        injection_volume6                      = self.worker.get_node("ns=2;i=20734").get_value()/10000
        injection_pos["injection_volume6"]     = {"value":-1,"edit":"none"}
        if numofseg >=6:
            injection_pos["injection_volume6"]     = {"value":injection_volume6,"edit":"none"}
        injection_volume7                      = self.worker.get_node("ns=2;i=20735").get_value()/10000
        injection_pos["injection_volume7"]     = {"value":-1,"edit":"none"}
        if numofseg >=7:
            injection_pos["injection_volume7"]     = {"value":injection_volume7,"edit":"none"}
        injection_volume8                      = self.worker.get_node("ns=2;i=20736").get_value()/10000
        injection_pos["injection_volume8"]     = {"value":-1,"edit":"none"}
        if numofseg >=8:
            injection_pos["injection_volume8"]     = {"value":injection_volume8,"edit":"none"}
        injection_volume9                      = self.worker.get_node("ns=2;i=20737").get_value()/10000
        injection_pos["injection_volume9"]     = {"value":-1,"edit":"none"}
        if numofseg >=9:
            injection_pos["injection_volume9"]     = {"value":injection_volume9,"edit":"none"}
        injection_volume10                      = self.worker.get_node("ns=2;i=20738").get_value()/10000
        injection_pos["injection_volume10"]     = {"value":-1,"edit":"none"}
        if numofseg >=10:
            injection_pos["injection_volume10"]     = {"value":injection_volume10,"edit":"none"}
        for k, v in injection_pos.items():
            if v["value"] == -1:
                injection_pos[k] = {"value": vp_position_set, "edit": "none"}
                break
        self.machinestatus["injection_pos"]    = injection_pos
        #Injection rate(speed) set
        injection_speed = {}
        injection_rate1_set                      = self.worker.get_node("ns=2;i=20741").get_value()/10000
        injection_speed["injection_rate1_set"]   = {"value":injection_rate1_set,"edit":"none"}
        injection_rate2_set                      = self.worker.get_node("ns=2;i=20742").get_value()/10000
        injection_speed["injection_rate2_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=2:
            injection_speed["injection_rate2_set"]   = {"value":injection_rate2_set,"edit":"none"}
        injection_rate3_set                      = self.worker.get_node("ns=2;i=20743").get_value()/10000
        injection_speed["injection_rate3_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=3:
            injection_speed["injection_rate3_set"]   = {"value":injection_rate3_set,"edit":"none"}
        injection_rate4_set                      = self.worker.get_node("ns=2;i=20744").get_value()/10000
        injection_speed["injection_rate4_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=4:
            injection_speed["injection_rate4_set"]   = {"value":injection_rate4_set,"edit":"none"}
        injection_rate5_set                      = self.worker.get_node("ns=2;i=20745").get_value()/10000
        injection_speed["injection_rate5_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=5:
            injection_speed["injection_rate5_set"]   = {"value":injection_rate5_set,"edit":"none"}
        injection_rate6_set                      = self.worker.get_node("ns=2;i=20746").get_value()/10000
        injection_speed["injection_rate6_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=6:
            injection_speed["injection_rate6_set"]   = {"value":injection_rate6_set,"edit":"none"}
        injection_rate7_set                      = self.worker.get_node("ns=2;i=20747").get_value()/10000
        injection_speed["injection_rate7_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=7:
            injection_speed["injection_rate7_set"]   = {"value":injection_rate7_set,"edit":"none"}
        injection_rate8_set                      = self.worker.get_node("ns=2;i=20748").get_value()/10000
        injection_speed["injection_rate8_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=8:
            injection_speed["injection_rate8_set"]   = {"value":injection_rate8_set,"edit":"none"}
        injection_rate9_set                      = self.worker.get_node("ns=2;i=20749").get_value()/10000
        injection_speed["injection_rate9_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=9:
            injection_speed["injection_rate9_set"]   = {"value":injection_rate9_set,"edit":"none"}
        injection_rate10_set                      = self.worker.get_node("ns=2;i=20750").get_value()/10000
        injection_speed["injection_rate10_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=10:
            injection_speed["injection_rate10_set"]   = {"value":injection_rate10_set,"edit":"none"}
        self.machinestatus["injection_speed"]    = injection_speed
        # Filling Time
        filling_time_set = self.worker.get_node("ns=2;i=20755").get_value()/1000
        self.machinestatus["filling_time_set"]    = {"value":filling_time_set,"edit":"none"}
        # Cooling time
        cooling_time                          = self.worker.get_node("ns=2;i=20708").get_value()/1000
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"none"}
        # Injection pressure setting
        injection_pressure_set                       = self.worker.get_node("ns=2;i=20752").get_value()/1000
        self.machinestatus["injection_pressure_set"] = {"value":injection_pressure_set,"edit":"none"}
        #Clamp force set
        clamp_force_set                        = self.worker.get_node("ns=2;i=21082").get_value() /100
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"none"}
        # Storage Pressure 
        if processstatus is True:
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
            # Collect Realtime IJ presure
            actijpressure = self.worker.get_node("ns=2;i=20684").get_value()/1000
            self.actpressurecurve.append(actijpressure)
            # Collect real time IJ speed
            actijspeed = self.worker.get_node("ns=2;i=20702").get_value()/1000
            self.actspeedcurve.append(actijspeed)
            # Collect screw position curve
            self.machinecurve["actpressurecurve"] = self.actpressurecurve
            self.machinecurve["actspeedcurve"]    = self.actspeedcurve
        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                print("[Message] Save data ...")
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
                self.screwposition    = []
                self.processactivate = False
                self.has_plastic = False
        #Get current time
        current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'{self.machineid}_updatetime',current_time)
        self.red.set(f'{self.machineid}_status',json.dumps(self.machinestatus))
        self.red.set(f'{self.machineid}_feedback',json.dumps(self.machinefeedback))
        self.red.set(f'{self.machineid}_curve',json.dumps(self.machinecurve))
if __name__ == "__main__":
    machineaddress = '10.10.150.3:4842'
    FCS            = fcsagent(machineaddress,'FCS-CT120')
    FCS.connect()
    while True:
      try:
        FCS.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




