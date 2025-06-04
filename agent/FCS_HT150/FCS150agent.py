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
    def __init__(self,machineaddress,user,password,machineid):
        self.rabbitmq_account  = "cax"
        self.rabbitmq_password = "cax521"
        self.hostip            = "192.168.1.225"
        self.machineid         = machineid
        self.machineaddress    = machineaddress
        self.user              = user
        self.password          = password
        self.processactivate   = False
        self.worker            = ""
        self.red = redis.Redis(host='192.168.1.225',port=6379,db=0)
        self.actpressurecurve = []
        self.actspeedcurve    = []
        self.screwposition    = []
        self.machinestatus    = {}
        self.machinefeedback  = {}
        self.machinecurve     = {}
        self.db = create_engine("postgresql://postgres:postgres@192.168.1.225:5432/cax")
        self.nodemap = {
            "holding_time1_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rStartPos','factor':1,'type':'float'},
            "holding_time2_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rStartPos','factor':1,'type':'float'},
            "holding_time3_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rStartPos','factor':1,'type':'float'},
            "holding_time4_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rStartPos','factor':1,'type':'float'},
            "holding_time5_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rStartPos','factor':1,'type':'float'},
            "holding_time6_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rStartPos','factor':1,'type':'float'},
            "holding_time7_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rStartPos','factor':1,'type':'float'},
            "holding_time8_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rStartPos','factor':1,'type':'float'},
            "holding_time9_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rStartPos','factor':1,'type':'float'},
            "holding_pressure1_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[1].rPressure','factor':13.05,'type':'float'},
            "holding_pressure2_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rPressure','factor':13.05,'type':'float'},
            "holding_pressure3_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rPressure','factor':13.05,'type':'float'},
            "holding_pressure4_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rPressure','factor':13.05,'type':'float'},
            "holding_pressure5_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rPressure','factor':13.05,'type':'float'},
            "holding_pressure6_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rPressure','factor':13.05,'type':'float'},
            "holding_pressure7_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rPressure','factor':13.05,'type':'float'},
            "holding_pressure8_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rPressure','factor':13.05,'type':'float'},
            "holding_pressure9_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rPressure','factor':13.05,'type':'float'},
            "holding_pressure10_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rPressure','factor':13.05,'type':'float'},
            "injection_volume1":{'nodeid':'ns=4;s=APPL.Injection1.sv_CutOffParams.rDetectionPositionLimit','factor':1.5204,'type':'float'},
            "injection_volume2":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume3":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume4":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume5":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume6":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume7":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume8":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume9":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rStartPos','factor':1.5204,'type':'float'},
            "injection_volume10":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rStartPos','factor':1.5204,'type':'float'},
            "injection_rate1_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[1].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate2_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate3_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate4_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate5_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate6_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate7_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate8_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate9_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rVelocity','factor':1.5204,'type':'float'},
            "injection_rate10_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rVelocity','factor':1.5204,'type':'float'},
            "injection_pressure1_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[1].rPressure','factor':13.05,'type':'float'},
            "injection_pressure2_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rPressure','factor':13.05,'type':'float'},
            "injection_pressure3_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rPressure','factor':13.05,'type':'float'},
            "injection_pressure4_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rPressure','factor':13.05,'type':'float'},
            "injection_pressure5_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rPressure','factor':13.05,'type':'float'},
            "injection_pressure6_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rPressure','factor':13.05,'type':'float'},
            "injection_pressure7_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rPressure','factor':13.05,'type':'float'},
            "injection_pressure8_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rPressure','factor':13.05,'type':'float'},
            "injection_pressure9_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rPressure','factor':13.05,'type':'float'},
            "injection_pressure10_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rPressure','factor':13.05,'type':'float'},
            "backpressure1":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[1].rBackPressure','factor':1,'type':'float'},
            "backpressure2":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[2].rBackPressure','factor':1,'type':'float'},
            "backpressure3":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[3].rBackPressure','factor':1,'type':'float'},
            "backpressure4":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[4].rBackPressure','factor':1,'type':'float'},
            "backpressure5":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[5].rBackPressure','factor':1,'type':'float'},
            "backpressure6":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[6].rBackPressure','factor':1,'type':'float'},
            "backpressure7":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[7].rBackPressure','factor':1,'type':'float'},
            "backpressure8":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[8].rBackPressure','factor':1,'type':'float'},
            "backpressure9":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[9].rBackPressure','factor':1,'type':'float'},
            "backpressure10":{'nodeid':'ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[10].rBackPressure','factor':1,'type':'float'},
            "clamp_force_set":{'nodeid':'ns=4;s=APPL.Mold1.sv_ClampForce.rSetClampForce','factor':1,'type':'float'},
            "filling_time_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_CutOffParams.dTimeThreshold','factor':1000000,'type':'int64'},
            "cooling_time":{'nodeid':'ns=4;s=APPL.CoolingTime1.sv_dCoolingTime','factor':1000000,'type':'int64'},
            "storage_pressure_set":{'nodeid':'ns=4;s=APPL.Injection1.sv_ConstChargePressure.Output.rOutputValue','factor':1,'type':'float'},
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
            data_value.ServerTimestamp = None
            data_value.SourceTimestamp = None
            data_value.StatusCode = ua.StatusCode(ua.StatusCodes.Good)
            self.worker.get_node(nodeid).set_value(data_value)
            
        

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
        processstatus                      = self.worker.get_node("ns=4;s=APPL.Injection1.do_Inject").get_value()
        # barrel temp
        barrel_temp_set = {}
        barrel_temp1_set                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain1.rSetValVis").get_value()
        barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temp1_set,"edit":"none"}
        barrel_temp2_set                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain2.rSetValVis").get_value()
        barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temp2_set,"edit":"none"}
        barrel_temp3_set                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain3.rSetValVis").get_value()
        barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temp3_set,"edit":"none"}
        barrel_temp4_set                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain4.rSetValVis").get_value()
        barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temp4_set,"edit":"none"}
        self.machinestatus["barrel_temp_set"] = barrel_temp_set

        barrel_temp_real = {}
        barrel_temp1_real                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp1").get_value()
        barrel_temp_real["barrel_temp1_real"]  = {"value":barrel_temp1_real,"edit":"none"}
        barrel_temp2_real                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp2").get_value()
        barrel_temp_real["barrel_temp2_real"]  = {"value":barrel_temp2_real,"edit":"none"}
        barrel_temp3_real                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp3").get_value()
        barrel_temp_real["barrel_temp3_real"]  = {"value":barrel_temp3_real,"edit":"none"}
        barrel_temp4_real                      = self.worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp4").get_value()
        barrel_temp_real["barrel_temp4_real"]  = {"value":barrel_temp4_real,"edit":"none"}
        self.machinestatus["barrel_temp_real"] = barrel_temp_real

        holdseg = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.iNoOfPoints").get_value()
        #Holding pressure & time setting
        holdingtimeset = {}
        holding_time1_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rStartPos").get_value()
        holdingtimeset["holding_time1_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 2:
            holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"acctivate"}
        holding_time2_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rStartPos").get_value()
        holdingtimeset["holding_time2_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 3:
            holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"acctivate"}
        holding_time3_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rStartPos").get_value()
        holdingtimeset["holding_time3_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 4:
            holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"acctivate"}
        holding_time4_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rStartPos").get_value()
        holdingtimeset["holding_time4_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 5:
            holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"acctivate"}
        holding_time5_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rStartPos").get_value()
        holdingtimeset["holding_time5_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 6:
            holdingtimeset["holding_time5_set"]     = {"value":holding_time5_set,"edit":"acctivate"}
        holding_time6_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rStartPos").get_value()
        holdingtimeset["holding_time6_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 7:
            holdingtimeset["holding_time6_set"]     = {"value":holding_time6_set,"edit":"acctivate"}
        holding_time7_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rStartPos").get_value()
        holdingtimeset["holding_time7_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 8:
            holdingtimeset["holding_time7_set"]     = {"value":holding_time7_set,"edit":"acctivate"}
        holding_time8_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rStartPos").get_value()
        holdingtimeset["holding_time8_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 9:
            holdingtimeset["holding_time8_set"]     = {"value":holding_time8_set,"edit":"acctivate"}
        holding_time9_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rStartPos").get_value()
        holdingtimeset["holding_time9_set"]     = {"value":-1,"edit":"none"}
        if holdseg >= 10:
            holdingtimeset["holding_time9_set"]     = {"value":holding_time9_set,"edit":"acctivate"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset

        holdingpressureset ={}
        holding_pressure1_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[1].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"acctivate"}
        holding_pressure2_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure2_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 2:
            holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"acctivate"}
        holding_pressure3_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure3_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 3:
            holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"acctivate"}
        holding_pressure4_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure4_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 4:
            holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"acctivate"}
        holding_pressure5_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure5_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 5:
            holdingpressureset["holding_pressure5_set"] = {"value":holding_pressure5_set,"edit":"acctivate"}
        holding_pressure6_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure6_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 6:
            holdingpressureset["holding_pressure6_set"] = {"value":holding_pressure6_set,"edit":"acctivate"}
        holding_pressure7_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure7_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 7:
            holdingpressureset["holding_pressure7_set"] = {"value":holding_pressure7_set,"edit":"acctivate"}
        holding_pressure8_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure8_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 8:
            holdingpressureset["holding_pressure8_set"] = {"value":holding_pressure8_set,"edit":"acctivate"}
        holding_pressure9_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure9_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 9:
            holdingpressureset["holding_pressure9_set"] = {"value":holding_pressure9_set,"edit":"acctivate"}
        holding_pressure10_set                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rPressure").get_value()/13.05
        holdingpressureset["holding_pressure10_set"] = {"value":-1,"edit":"none"}
        if holdseg >= 10:
            holdingpressureset["holding_pressure10_set"] = {"value":holding_pressure10_set,"edit":"acctivate"}
        self.machinestatus["holdingpressureset"]    = holdingpressureset
        numofseg = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.iNoOfPoints").get_value()
        # Back pressure
        backpressure  = {}
        numofbackpressureuse = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.iNoOfPoints").get_value()
        backpressure1                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[1].rBackPressure").get_value()
        backpressure["backpressure1"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=1:
            backpressure["backpressure1"]       = {"value":backpressure1,"edit":"acctivate"}
        backpressure2                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[2].rBackPressure").get_value()
        backpressure["backpressure2"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=2:
            backpressure["backpressure2"]       = {"value":backpressure2,"edit":"acctivate"}
        backpressure3                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[3].rBackPressure").get_value()
        backpressure["backpressure3"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=3:
            backpressure["backpressure3"]       = {"value":backpressure3,"edit":"acctivate"}
        backpressure4                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[4].rBackPressure").get_value()
        backpressure["backpressure4"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=4:
            backpressure["backpressure4"]       = {"value":backpressure4,"edit":"acctivate"}
        backpressure5                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[5].rBackPressure").get_value()
        backpressure["backpressure5"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=5:
            backpressure["backpressure5"]       = {"value":backpressure5,"edit":"acctivate"}
        backpressure6                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[6].rBackPressure").get_value()
        backpressure["backpressure6"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=6:
            backpressure["backpressure6"]       = {"value":backpressure6,"edit":"acctivate"}
        backpressure7                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[7].rBackPressure").get_value()
        backpressure["backpressure7"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=7:
            backpressure["backpressure7"]       = {"value":backpressure7,"edit":"acctivate"}
        backpressure8                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[8].rBackPressure").get_value()
        backpressure["backpressure8"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=8:
            backpressure["backpressure8"]       = {"value":backpressure8,"edit":"acctivate"}
        backpressure9                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[9].rBackPressure").get_value()
        backpressure["backpressure9"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=9:
            backpressure["backpressure9"]       = {"value":backpressure9,"edit":"acctivate"}
        backpressure10                       = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[10].rBackPressure").get_value()
        backpressure["backpressure10"]       = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=10:
            backpressure["backpressure10"]       = {"value":backpressure10,"edit":"acctivate"}
        self.machinestatus["backpressure"]  = backpressure
        # storage position 
        storagepos = []
        storage_position = {}
        storage_position1                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[2].rStartPos").get_value()/1.5204
        storage_position["storage_position1"]   = {"value":storage_position1,"edit":"acctivate"}
        storagepos.append(storage_position1)
        storage_position2                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[3].rStartPos").get_value()/1.5204
        storage_position["storage_position2"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=2:
            storage_position["storage_position2"]   = {"value":storage_position2,"edit":"acctivate"}
            storagepos.append(storage_position2)
        storage_position3                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[4].rStartPos").get_value()/1.5204
        storage_position["storage_position3"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=3:
            storage_position["storage_position3"]   = {"value":storage_position3,"edit":"acctivate"}
            storagepos.append(storage_position3)
        storage_position4                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[5].rStartPos").get_value()/1.5204
        storage_position["storage_position4"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=4:
            storage_position["storage_position4"]   = {"value":storage_position4,"edit":"acctivate"}
            storagepos.append(storage_position4)
        storage_position5                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[6].rStartPos").get_value()/1.5204
        storage_position["storage_position5"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=5:
            storage_position["storage_position5"]   = {"value":storage_position5,"edit":"acctivate"}
            storagepos.append(storage_position5)
        storage_position6                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[7].rStartPos").get_value()/1.5204
        storage_position["storage_position6"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=6:
            storage_position["storage_position6"]   = {"value":storage_position6,"edit":"acctivate"}
            storagepos.append(storage_position6)
        storage_position7                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[8].rStartPos").get_value()/1.5204
        storage_position["storage_position7"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=7:
            storage_position["storage_position7"]   = {"value":storage_position7,"edit":"acctivate"}
            storagepos.append(storage_position7)
        storage_position8                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[9].rStartPos").get_value()/1.5204
        storage_position["storage_position8"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=8:
            storage_position["storage_position8"]   = {"value":storage_position8,"edit":"acctivate"}
            storagepos.append(storage_position8)
        storage_position9                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[10].rStartPos").get_value()/1.5204
        storage_position["storage_position9"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=9:
            storage_position["storage_position9"]   = {"value":storage_position9,"edit":"acctivate"}
            storagepos.append(storage_position9)
        storage_position10                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_PlastProfVis.Profile.Points[11].rStartPos").get_value()/1.5204
        storage_position["storage_position10"]   = {"value":-1,"edit":"none"}
        if numofbackpressureuse >=10:
            storage_position["storage_position10"]   = {"value":storage_position10,"edit":"acctivate"}
            storagepos.append(storage_position10)
        ijvol1 = max(storagepos)
        self.machinestatus["storage_position"]  = storage_position           
        # Injection volume(position) set
        injection_pos ={}
        injection_pos["injection_volume1"]     = {"value":ijvol1,"edit":"none"}
        injection_volume2                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rStartPos").get_value()/1.5204
        injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"acctivate"}
        injection_volume3                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rStartPos").get_value()/1.5204
        injection_pos["injection_volume3"]     = {"value":-1,"edit":"none"}
        if numofseg >=3:
            injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"acctivate"}
        injection_volume4                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rStartPos").get_value()/1.5204
        injection_pos["injection_volume4"]     = {"value":-1,"edit":"none"}
        if numofseg >=4:
            injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"acctivate"}
        injection_volume5                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rStartPos").get_value()/1.5204
        injection_pos["injection_volume5"]     = {"value":-1,"edit":"none"}
        if numofseg >=5:
            injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"acctivate"}
        injection_volume6                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rStartPos").get_value()/1.5204
        injection_pos["injection_volume6"]     = {"value":-1,"edit":"none"}
        if numofseg >=6:
            injection_pos["injection_volume6"]     = {"value":injection_volume6,"edit":"acctivate"}
        injection_volume7                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rStartPos").get_value()/1.5204
        injection_pos["injection_volume7"]     = {"value":-1,"edit":"none"}
        if numofseg >=7:
            injection_pos["injection_volume7"]     = {"value":injection_volume7,"edit":"acctivate"}
        injection_volume8                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rStartPos").get_value()/1.5204
        injection_pos["injection_volume8"]     = {"value":-1,"edit":"none"}
        if numofseg >=8:
            injection_pos["injection_volume8"]     = {"value":injection_volume8,"edit":"acctivate"}
        injection_volume9                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rStartPos").get_value()/1.5204
        injection_pos["injection_volume9"]     = {"value":-1,"edit":"none"}
        if numofseg >=9:
            injection_pos["injection_volume9"]     = {"value":injection_volume9,"edit":"acctivate"}
        injection_volume10                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rStartPos").get_value()/1.5204
        injection_pos["injection_volume10"]     = {"value":-1,"edit":"none"}
        if numofseg >=10:
            injection_pos["injection_volume10"]     = {"value":injection_volume10,"edit":"acctivate"}
        self.machinestatus["injection_pos"]    = injection_pos
        #Injection rate(speed) set
        injection_speed = {}
        injection_rate1_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[1].rVelocity").get_value()/1.5204
        injection_speed["injection_rate1_set"]   = {"value":injection_rate1_set,"edit":"acctivate"}
        injection_rate2_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rVelocity").get_value()/1.5204
        injection_speed["injection_rate2_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=2:
            injection_speed["injection_rate2_set"]   = {"value":injection_rate2_set,"edit":"acctivate"}
        injection_rate3_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rVelocity").get_value()/1.5204
        injection_speed["injection_rate3_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=3:
            injection_speed["injection_rate3_set"]   = {"value":injection_rate3_set,"edit":"acctivate"}
        injection_rate4_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rVelocity").get_value()/1.5204
        injection_speed["injection_rate4_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=4:
            injection_speed["injection_rate4_set"]   = {"value":injection_rate4_set,"edit":"acctivate"}
        injection_rate5_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rVelocity").get_value()/1.5204
        injection_speed["injection_rate5_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=5:
            injection_speed["injection_rate5_set"]   = {"value":injection_rate5_set,"edit":"acctivate"}
        injection_rate6_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rVelocity").get_value()/1.5204
        injection_speed["injection_rate6_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=6:
            injection_speed["injection_rate6_set"]   = {"value":injection_rate6_set,"edit":"acctivate"}
        injection_rate7_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rVelocity").get_value()/1.5204
        injection_speed["injection_rate7_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=7:
            injection_speed["injection_rate7_set"]   = {"value":injection_rate7_set,"edit":"acctivate"}
        injection_rate8_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rVelocity").get_value()/1.5204
        injection_speed["injection_rate8_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=8:
            injection_speed["injection_rate8_set"]   = {"value":injection_rate8_set,"edit":"acctivate"}
        injection_rate9_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rVelocity").get_value()/1.5204
        injection_speed["injection_rate9_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=9:
            injection_speed["injection_rate9_set"]   = {"value":injection_rate9_set,"edit":"acctivate"}
        injection_rate10_set                      = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rVelocity").get_value()/1.5204
        injection_speed["injection_rate10_set"]   = {"value":-1,"edit":"none"}
        if numofseg >=10:
            injection_speed["injection_rate10_set"]   = {"value":injection_rate10_set,"edit":"acctivate"}
        self.machinestatus["injection_speed"]    = injection_speed
        # Filling Time
        filling_time_set = self.worker.get_node("ns=4;s=APPL.Injection1.sv_CutOffParams.dTimeThreshold").get_value()/1000000
        self.machinestatus["filling_time_set"]    = {"value":filling_time_set,"edit":"acctivate"}
        # Cooling time
        cooling_time                          = self.worker.get_node("ns=4;s=APPL.CoolingTime1.sv_dCoolingTime").get_value()/1000000
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"acctivate"}
        # Injection pressure setting
        injection_pressure_list                            = {}
        injection_pressure1_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[1].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure1_set"] = {"value":injection_pressure1_set,"edit":"acctivate"}
        injection_pressure2_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure2_set"] = {"value":-1,"edit":"none"}
        if numofseg >=2:
            injection_pressure_list["injection_pressure2_set"] = {"value":injection_pressure2_set,"edit":"acctivate"}
        injection_pressure3_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure3_set"] = {"value":-1,"edit":"none"}
        if numofseg >=3:
            injection_pressure_list["injection_pressure3_set"] = {"value":injection_pressure3_set,"edit":"acctivate"}      
        injection_pressure4_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure4_set"] = {"value":-1,"edit":"none"}
        if numofseg >=4:
            injection_pressure_list["injection_pressure4_set"] = {"value":injection_pressure4_set,"edit":"acctivate"}         
        injection_pressure5_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure5_set"] = {"value":-1,"edit":"none"}  
        if numofseg >=5:
            injection_pressure_list["injection_pressure5_set"] = {"value":injection_pressure5_set,"edit":"acctivate"}        
        injection_pressure6_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure6_set"] = {"value":-1,"edit":"none"}  
        if numofseg >=6:
            injection_pressure_list["injection_pressure6_set"] = {"value":injection_pressure6_set,"edit":"acctivate"}          
        injection_pressure7_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure7_set"] = {"value":-1,"edit":"none"}
        if numofseg >=7:
            injection_pressure_list["injection_pressure7_set"] = {"value":injection_pressure7_set,"edit":"acctivate"}
        injection_pressure8_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure8_set"] = {"value":-1,"edit":"none"}
        if numofseg >=8:
            injection_pressure_list["injection_pressure8_set"] = {"value":injection_pressure8_set,"edit":"acctivate"}
        injection_pressure9_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure9_set"] = {"value":-1,"edit":"none"}   
        if numofseg >=9:
            injection_pressure_list["injection_pressure9_set"] = {"value":injection_pressure9_set,"edit":"acctivate"}
        injection_pressure10_set                            = self.worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rPressure").get_value()/13.05
        injection_pressure_list["injection_pressure10_set"] = {"value":-1,"edit":"none"}
        if numofseg >=10:
            injection_pressure_list["injection_pressure10_set"] = {"value":injection_pressure10_set,"edit":"acctivate"}                
        self.machinestatus["injection_pressure_list"]      = injection_pressure_list
        #Clamp force set
        clamp_force_set                        = self.worker.get_node("ns=4;s=APPL.Mold1.sv_ClampForce.rSetClampForce").get_value()
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"acctivate"}
        # Storage Pressure 
        storage_pressure_set                   = self.worker.get_node("ns=4;s=APPL.Injection1.sv_ConstChargePressure.Output.rOutputValue").get_value()
        self.machinestatus["storage_pressure_set"]  = {"value":storage_pressure_set,"edit":"acctivate"}
        if processstatus is True:
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
            # Collect Realtime IJ presure
            actijpressure = self.worker.get_node("ns=4;s=APPL.Injection1.ai_Pressure").get_value()*25.12
            self.actpressurecurve.append(actijpressure)
            # Collect real time IJ speed
            actijspeed = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rScrewVelocityAbs").get_value()
            self.actspeedcurve.append(actijspeed)
            # Collect screw position curve
            screw_position = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rScrewPositionAbs").get_value()
            self.screwposition.append(screw_position)
            self.machinecurve["actpressurecurve"] = self.actpressurecurve
            self.machinecurve["actspeedcurve"]    = self.actspeedcurve
            self.machinecurve["screwposition"]    = self.screwposition
        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                print("[Message] Save data ...")
                # Material Cushion (餘料)
                material_cushion                         = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rCushion").get_value()
                self.machinefeedback["material_cushion"] = material_cushion
                # Filling time
                filling_time                    = self.worker.get_node("ns=4;s=APPL.Injection1.sv_dActInjectTimeForPDP").get_value()/1000000
                self.machinefeedback["filling_time"] = filling_time
                # Maximun real injection pressure
                Maximun_real_injection_pressure                    = self.worker.get_node("ns=4;s=APPL.Injection1.ai_Pressure").get_value()*25.12
                self.machinefeedback["Maximun_real_injection_pressure"] = Maximun_real_injection_pressure
                # Maximun real injection speed
                maximun_real_injection_speed                    = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rScrewVelocityAbs").get_value()
                self.machinefeedback["maximun_real_injection_speed"] = maximun_real_injection_speed
                # VP position real
                vp_position_real                    = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rCutOffPosition").get_value()/1.5204
                self.machinefeedback["vp_position_real"] = vp_position_real
                # real vp pressure
                real_vp_pressure                    = self.worker.get_node("ns=4;s=APPL.Injection1.sv_rCutOffPressure").get_value()/1.5204
                self.machinefeedback["real_vp_pressure"] = real_vp_pressure
                self.processactivate =False
                # Act Cycle time 
                act_cycle_time = self.worker.get_node("ns=4;s=APPL.system.sv_dLastCycleTime").get_value()/1000000
                self.machinefeedback["act_cycle_time"] = act_cycle_time
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
        #Get current time
        current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'{self.machineid}_updatetime',current_time)
        self.red.set(f'{self.machineid}_status',json.dumps(self.machinestatus))
        self.red.set(f'{self.machineid}_feedback',json.dumps(self.machinefeedback))
        self.red.set(f'{self.machineid}_curve',json.dumps(self.machinecurve))
if __name__ == "__main__":
    machineaddress = '192.168.1.12:4842'
    user           = os.environ.get('user', 'localuser1622689641636')
    password       = os.environ.get('password', '12345')
    FCS            = fcsagent(machineaddress,user,password,'FCS-150')
    FCS.connect()
    while True:
      try:
        FCS.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




