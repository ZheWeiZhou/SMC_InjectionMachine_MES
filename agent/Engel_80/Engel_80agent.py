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

class engelagent:
    def __init__(self,machineaddress,user,password,machineid):
        self.rabbitmq_account = "cax"
        self.rabbitmq_password = "cax521"
        self.hostip = "192.168.1.50"
        self.machineid = machineid
        self.machineaddress = machineaddress
        self.user = user
        self.password = password
        self.processactivate = False
        self.worker = ""
        self.red = redis.Redis(host='192.168.1.50',port=6379,db=0)
        self.actpressurecurve = []
        self.actspeedcurve = []
        self.motorpower = []
        self.heaterpower= []
        self.screwposition = []
        self.timeindex = []
        self.machinestatus   = {}
        self.machinefeedback = {}
        self.machinecurve   = {}
        self.db=create_engine("postgresql://postgres:postgres@192.168.1.50:5432/cax")
        self.nodemap = {
            "holding_time1_set":"ns=5;i=61",
            "holding_pressure1_set":"ns=5;i=62",
            "holding_time2_set":"ns=5;i=63",
            "holding_pressure2_set":"ns=5;i=64",
            "holding_time3_set":"ns=5;i=65",
            "holding_pressure3_set":"ns=5;i=66",
            "holding_time4_set":"ns=5;i=67",
            "holding_pressure4_set":"ns=5;i=68",
            "injection_volume1":"ns=5;i=94",
            "injection_volume2":"ns=5;i=73",
            "injection_volume3":"ns=5;i=75",
            "injection_volume4":"ns=5;i=77",
            "injection_volume5":"ns=5;i=79",
            "injection_rate1_set":"ns=5;i=72",
            "injection_rate2_set":"ns=5;i=74",
            "injection_rate3_set":"ns=5;i=76",
            "injection_rate4_set":"ns=5;i=78",
            "injection_rate5_set":"ns=5;i=80",
            "vp_position_set":"ns=5;i=51",
            "cooling_time":"ns=5;i=100",
            "injection_pressure_set":"ns=5;i=96",
            "backpressure1":"ns=5;i=58",
            "backpressure2":"ns=5;i=59",
            "backpressure3":"ns=5;i=60",
            "clamp_force_set":"ns=5;i=29"
        }
        
    def connect(self):  
        url="opc.tcp://"+self.machineaddress
        self.worker=Client(url)
        try:
            self.worker.set_user(self.user)
            self.worker.set_password(self.password)
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
        except:
            print("[ERROR] Connect to Engel fail")
    
    def parametersetting(self,target,value):
        access_node = list(self.nodemap.keys())
        if target in access_node:
            nodeid = self.nodemap[target]
            value  = float(value) 
            self.worker.get_node(nodeid).set_value(ua.Variant(value, ua.VariantType.Float))
        

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
        processstatus                      = self.worker.get_node("ns=1;i=77").get_value()
        #Holding pressure & time setting
        holdingtimeset = {}
        holding_time1_set                       = self.worker.get_node("ns=5;i=61").get_value()
        holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"acctivate"}
        holding_time2_set                       = self.worker.get_node("ns=5;i=63").get_value()
        holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"acctivate"}
        holding_time3_set                       = self.worker.get_node("ns=5;i=65").get_value()
        holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"acctivate"}
        holding_time4_set                       = self.worker.get_node("ns=5;i=67").get_value()
        holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"acctivate"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset

        holdingpressureset ={}
        holding_pressure1_set                       = self.worker.get_node("ns=5;i=62").get_value()
        holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"acctivate"}
        holding_pressure2_set                       = self.worker.get_node("ns=5;i=64").get_value()
        holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"acctivate"}
        holding_pressure3_set                       = self.worker.get_node("ns=5;i=66").get_value()
        holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"acctivate"}
        holding_pressure4_set                       = self.worker.get_node("ns=5;i=68").get_value()
        holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"acctivate"}
        self.machinestatus["holdingpressureset"]    = holdingpressureset
        #Injection volume(position) set
        injection_pos ={}
        injection_volume1                      = self.worker.get_node("ns=5;i=94").get_value()
        injection_pos["injection_volume1"]     = {"value":injection_volume1,"edit":"acctivate"}
        injection_volume2                      = self.worker.get_node("ns=5;i=73").get_value()
        injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"acctivate"}
        injection_volume3                      = self.worker.get_node("ns=5;i=75").get_value()
        injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"acctivate"}
        injection_volume4                      = self.worker.get_node("ns=5;i=77").get_value()
        injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"acctivate"}
        injection_volume5                      = self.worker.get_node("ns=5;i=79").get_value()
        injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"acctivate"}
        self.machinestatus["injection_pos"]    = injection_pos
        #Injection rate(speed) set
        injection_speed = {}
        injection_rate1_set                       = self.worker.get_node("ns=5;i=72").get_value()
        injection_speed["injection_rate1_set"]    = {"value":injection_rate1_set,"edit":"acctivate"}
        injection_rate2_set                       = self.worker.get_node("ns=5;i=74").get_value()
        injection_speed["injection_rate2_set"]    = {"value":injection_rate2_set,"edit":"acctivate"}
        injection_rate3_set                       = self.worker.get_node("ns=5;i=76").get_value()
        injection_speed["injection_rate3_set"]    = {"value":injection_rate3_set,"edit":"acctivate"}
        injection_rate4_set                       = self.worker.get_node("ns=5;i=78").get_value()
        injection_speed["injection_rate4_set"]    = {"value":injection_rate4_set,"edit":"acctivate"}
        injection_rate5_set                       = self.worker.get_node("ns=5;i=80").get_value()
        injection_speed["injection_rate5_set"]    = {"value":injection_rate5_set,"edit":"acctivate"}
        self.machinestatus["injection_speed"]     = injection_speed

        #VP position setting
        vp_position_set                       = self.worker.get_node("ns=5;i=51").get_value()
        self.machinestatus["vp_position_set"] = {"value":vp_position_set,"edit":"acctivate"}
        #Cooling time
        cooling_time                          = self.worker.get_node("ns=5;i=100").get_value()
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"acctivate"}
        #Injection pressure setting
        injection_pressure_set                       = self.worker.get_node("ns=5;i=96").get_value()
        self.machinestatus["injection_pressure_set"] = {"value":injection_pressure_set,"edit":"acctivate"}
        #Back pressure
        backpressure  = {}
        backpressure1                       = self.worker.get_node("ns=5;i=58").get_value()
        backpressure["backpressure1"]       = {"value":backpressure1,"edit":"acctivate"}
        backpressure2                       = self.worker.get_node("ns=5;i=59").get_value()
        backpressure["backpressure2"]       = {"value":backpressure2,"edit":"acctivate"}
        backpressure3                       = self.worker.get_node("ns=5;i=60").get_value()
        backpressure["backpressure3"]       = {"value":backpressure3,"edit":"acctivate"}
        self.machinestatus["backpressure"]  = backpressure
        #Clamp force set
        clamp_force_set                        = self.worker.get_node("ns=5;i=29").get_value()
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"acctivate"}

        if processstatus == 4:
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
            # #Collect Realtime IJ presure
            actijpressure = self.worker.get_node("ns=5;i=53").get_value()
            self.actpressurecurve.append(actijpressure)
            # #Collect real time IJ speed
            actijspeed = self.worker.get_node("ns=5;i=55").get_value()
            self.actspeedcurve.append(actijspeed)
            # Get ACT motor power
            actmotorpower = self.worker.get_node("ns=5;i=48").get_value()
            self.motorpower.append(actmotorpower)
            #Get ACT heater power
            actheaterpower = self.worker.get_node("ns=5;i=47").get_value()
            self.heaterpower.append(actheaterpower)

            self.machinecurve["actpressurecurve"] = self.actpressurecurve
            self.machinecurve["actspeedcurve"]    = self.actspeedcurve
            self.machinecurve["motorpower"]       = self.motorpower
            self.machinecurve["heaterpower"]      = self.heaterpower

        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                print("[Message] Save data ...")
                # Material Cushion (餘料)
                material_cushion                         = self.worker.get_node("ns=5;i=90").get_value()
                self.machinefeedback["material_cushion"] = material_cushion
                # Screw volume
                screw_volume                    = self.worker.get_node("ns=1;i=148").get_value()
                self.machinefeedback["screw_volume"] = screw_volume
                #Filling time
                filling_time                    = self.worker.get_node("ns=5;i=52").get_value()
                self.machinefeedback["filling_time"] = filling_time
                #Maximun real injection pressure
                Maximun_real_injection_pressure                    = self.worker.get_node("ns=5;i=56").get_value()
                self.machinefeedback["Maximun_real_injection_pressure"] = Maximun_real_injection_pressure
                #Maximun real injection speed
                maximun_real_injection_speed                    = self.worker.get_node("ns=5;i=57").get_value()
                self.machinefeedback["maximun_real_injection_speed"] = maximun_real_injection_speed
                #Filling start position
                filling_start_position                    = self.worker.get_node("ns=4;i=6164").get_value()
                self.machinefeedback["filling_start_position"] = filling_start_position
                #VP position real
                vp_position_real                    = self.worker.get_node("ns=5;i=92").get_value()
                self.machinefeedback["vp_position_real"] = vp_position_real
                storage_position                    = self.worker.get_node("ns=5;i=63").get_value()
                self.machinefeedback["storage_position"] = storage_position
                #real vp pressure
                real_vp_pressure                    = self.worker.get_node("ns=5;i=93").get_value()
                self.machinefeedback["real_vp_pressure"] = real_vp_pressure
                #Act plastic time
                act_plastic_time                    = self.worker.get_node("ns=5;i=89").get_value()
                self.machinefeedback["act_plastic_time"] = act_plastic_time
                #Act cycle time
                act_cycle_time                    = self.worker.get_node("ns=5;i=30").get_value()
                self.machinefeedback["act_cycle_time"] = act_cycle_time
                #Maximun_screw_torque
                maximun_screw_torque                    = self.worker.get_node("ns=5;i=98").get_value()
                self.machinefeedback["maximun_screw_torque"] = maximun_screw_torque
                #Mean_screw_torque
                mean_screw_torque                    = self.worker.get_node("ns=5;i=97").get_value()
                self.machinefeedback["mean_screw_torque"] = mean_screw_torque
                # Motor Energy (KWH)
                motorenergy                    = self.worker.get_node("ns=5;i=33").get_value()
                self.machinefeedback["motorenergy"] = motorenergy
                # Heater Engery (KWH)
                heaterenergy                    = self.worker.get_node("ns=5;i=31").get_value()
                self.machinefeedback["heaterenergy"] = heaterenergy
                # Oil Motor Energy (KWH)
                Oilmotorenergy                    = self.worker.get_node("ns=5;i=46").get_value()
                self.machinefeedback["Oilmotorenergy"] = Oilmotorenergy
                # Injection Motor Energy (KWH)
                injectionmotorenergy                    = self.worker.get_node("ns=5;i=44").get_value()
                self.machinefeedback["injectionmotorenergy"] = injectionmotorenergy
                # Plastic Motor Energy (KWH)
                plasticmotorenergy                    = self.worker.get_node("ns=5;i=45").get_value()
                self.machinefeedback["plasticmotorenergy"] = plasticmotorenergy
                # Close Mold Energy (KWH)
                closemoldenergy                    = self.worker.get_node("ns=5;i=37").get_value()
                self.machinefeedback["closemoldenergy"] = closemoldenergy
                # Nozzle Energy
                nozzle_energy                    = self.worker.get_node("ns=5;i=39").get_value()
                self.machinefeedback["nozzle_energy"] = nozzle_energy
                # Injection Energy
                injection_energy                    = self.worker.get_node("ns=5;i=40").get_value()
                self.machinefeedback["injection_energy"] = injection_energy
                # Holding Energy
                holdingenergy                    = self.worker.get_node("ns=5;i=41").get_value()
                self.machinefeedback["holdingenergy"] = holdingenergy
                # Cooling Energy
                coolingenergy                    = self.worker.get_node("ns=5;i=43").get_value()
                self.machinefeedback["coolingenergy"] = coolingenergy
                # Plastic Energy
                plasticenergy                    = self.worker.get_node("ns=5;i=42").get_value()
                self.machinefeedback["plasticenergy"] = plasticenergy
                #Open mold energy
                openmoldenergy                    = self.worker.get_node("ns=5;i=38").get_value()
                self.machinefeedback["openmoldenergy"] = openmoldenergy
                #Eject energy
                ejectenergy                    = self.worker.get_node("ns=5;i=34").get_value()
                self.machinefeedback["ejectenergy"] = ejectenergy
                #semi auto energy
                semi_energy                    = self.worker.get_node("ns=5;i=36").get_value()
                self.machinefeedback["semi_energy"] = semi_energy
                # Core energy
                core_energy                    = self.worker.get_node("ns=5;i=35").get_value()
                self.machinefeedback["core_energy"] = core_energy
                # IQ VP
                iqvp                    = self.worker.get_node("ns=5;i=49").get_value()
                self.machinefeedback["iqvp"] = iqvp
                # IQ Holding Pressure
                iqhp                    = self.worker.get_node("ns=5;i=50").get_value()
                self.machinefeedback["iqhp"] = iqhp

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
                self.actpressurecurve=[]
                self.actspeedcurve=[]
                self.motorpower=[]
                self.heaterpower=[]
                self.screwposition =[]
                self.timeindex =[]
        #Get current time
        current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'{self.machineid}_updatetime',current_time)
        self.red.set(f'{self.machineid}_status',json.dumps(self.machinestatus))
        self.red.set(f'{self.machineid}_feedback',json.dumps(self.machinefeedback))
        self.red.set(f'{self.machineid}_curve',json.dumps(self.machinecurve))
if __name__ == "__main__":
    machineaddress = '192.168.1.16:4840'
    user           = os.environ.get('user','localuser1585892241043')
    password       = os.environ.get('password','smc499')
    Engel          = engelagent(machineaddress,user,password,'Engel-80')
    Engel.connect()
    while True:
      try:
        Engel.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




