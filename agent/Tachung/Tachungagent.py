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
import base64
Base = declarative_base()
class injection_machine_db(Base):
    __tablename__    = "MachineHistory"
    id               = Column(Integer, primary_key=True)
    created_at       = Column(TIMESTAMP)
    machine_name     = Column(TEXT)
    machine_status   = Column(TEXT)
    machine_feedback = Column(TEXT)
    machine_curve    = Column(TEXT)

class tachungagent:
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
            "clamp_force_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmblmG7yRXheItZIfkBnub4CU6pOwscKrvIXmZ7SdShvEjcek=",
            "holding_time1_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJcfCI2C96i1x6Q==",
            "holding_time2_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJsfCI2C96i1x6Q==",
            "holding_time3_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJ8fCI2C96i1x6Q==",
            "holding_time4_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIMfCI2C96i1x6Q==",
            "holding_time5_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIcfCI2C96i1x6Q==",
            "holding_pressure1_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJcfTMnGa8DVmjIM=",
            "holding_pressure2_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJsfTMnGa8DVmjIM=",
            "holding_pressure3_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJ8fTMnGa8DVmjIM=",
            "holding_pressure4_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIMfTMnGa8DVmjIM=",
            "holding_pressure5_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIcfTMnGa8DVmjIM=",
            "injection_volume1":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfTL2eA9yl7h4M=",
            "injection_volume2":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfTL2eA9yl7h4M=",
            "injection_volume3":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fTL2eA9yl7h4M=",
            "injection_volume4":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfTL2eA9yl7h4M=",
            "injection_volume5":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfTL2eA9yl7h4M=",
            "injection_volume6":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfTL2eA9yl7h4M=",
            "injection_rate1_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfQMHGM50A=",
            "injection_rate2_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfQMHGM50A=",
            "injection_rate3_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fQMHGM50A=",
            "injection_rate4_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfQMHGM50A=",
            "injection_rate5_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfQMHGM50A=",
            "injection_rate6_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfQMHGM50A=",
            "cooling_time":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itA3uG7yl6jtcpeYyD",
            "vp_position_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo6tBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo7TL2eA9yl7h4M=",
            "filling_time_limit_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo6tBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo7XKXmMgw==",
            "injection_pressure1_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfTMnGa8DVmjIM=",
            "injection_pressure2_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfTMnGa8DVmjIM=",
            "injection_pressure3_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fTMnGa8DVmjIM=",
            "injection_pressure4_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfTMnGa8DVmjIM=",
            "injection_pressure5_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfTMnGa8DVmjIM=",
            "injection_pressure6_set":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfTMnGa8DVmjIM=",
            "backpressure1":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrJuRJvmM2ec8SUU",
            "backpressure2":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrFuRJvmM2ec8SUU",
            "backpressure3":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrBuRJvmM2ec8SUU",
            "backpressure4":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrduRJvmM2ec8SUU",
            "dos_position1":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrJuRJvmM2ec8SUU",
            "dos_position2":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrFuRIbwKWCA7C4U",
            "dos_position3":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrBuRIbwKWCA7C4U",
            "dos_position4":"ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrduRIbwKWCA7C4U",
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
            nodeid = self.nodemap[target]
            value  = float(value) 
            self.worker.get_node(self.get_node_safe(nodeid)).set_value(ua.Variant(value, ua.VariantType.Double))
            
        

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
    def get_node_safe(self, nodeid_str):
        if nodeid_str.startswith("ns=") and ";b=" in nodeid_str:
            # 處理 ByteString 類型的 NodeId
            ns_part, b64_part = nodeid_str.split(";b=")
            namespace_index = int(ns_part.split("=")[1])
            # 正確解碼 base64 成 bytes
            identifier_bytes = base64.b64decode(b64_part)
            nodeid = ua.NodeId(identifier_bytes, namespace_index, ua.NodeIdType.ByteString)
        else:
            # 字串型 NodeId 直接使用
            nodeid = nodeid_str
        return nodeid 
    def collectdata(self):
        # Check processstatus
        processstatus                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQ11iuspeozQNHWd9jM6pOIjfIDtJVmG5yUU")).get_value()
        # barrel temp
        barrel_temp_set = {}
        barrel_temp1_set                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxxOqfsLX2H4ixAjO4wcZviNGGb5kA=")).get_value()
        barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temp1_set,"edit":"none"}

        barrel_temp2_set                      = self.worker.get_node( self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxyOqfsLX2H4ixAjO4wcZviNGGb5kA=")).get_value()
        barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temp2_set,"edit":"none"}
        barrel_temp3_set                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxzOqfsLX2H4ixAjO4wcZviNGGb5kA=")).get_value()
        barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temp3_set,"edit":"none"}
        barrel_temp4_set                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx0OqfsLX2H4ixAjO4wcZviNGGb5kA=")).get_value()
        barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temp4_set,"edit":"none"}
        barrel_temp5_set                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx1OqfsLX2H4ixAjO4wcZviNGGb5kA=")).get_value()
        barrel_temp_set["barrel_temp5_set"]   = {"value":barrel_temp5_set,"edit":"none"}
        # barrel_temp6_set                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx2OqfsLX2H4ixAjO4wcZviNGGb5kA=").get_value()
        # barrel_temp_set["barrel_temp6_set"]   = {"value":barrel_temp6_set,"edit":"none"}
        # barrel_temp7_set                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx3OqfsLX2H4ixAjO4wcZviNGGb5kA=").get_value()
        # barrel_temp_set["barrel_temp7_set"]   = {"value":barrel_temp7_set,"edit":"none"}
        # barrel_temp8_set                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx4OqfsLX2H4ixAjO4wcZviNGGb5kA=").get_value()
        # barrel_temp_set["barrel_temp8_set"]   = {"value":barrel_temp8_set,"edit":"none"}

        self.machinestatus["barrel_temp_set"] = barrel_temp_set

        barrel_temp_real = {}
        barrel_temp1_real                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxxOqjgNGGI7xRxhPMlZoj3NWaMgw==")).get_value()
        barrel_temp_real["barrel_temp1_real"]  = {"value":barrel_temp1_real,"edit":"none"}
        barrel_temp2_real                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxyOqjgNGGI7xRxhPMlZoj3NWaMgw==")).get_value()
        barrel_temp_real["barrel_temp2_real"]  = {"value":barrel_temp2_real,"edit":"none"}
        barrel_temp3_real                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNxzOqjgNGGI7xRxhPMlZoj3NWaMgw==")).get_value()
        barrel_temp_real["barrel_temp3_real"]  = {"value":barrel_temp3_real,"edit":"none"}
        barrel_temp4_real                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx0OqjgNGGI7xRxhPMlZoj3NWaMgw==")).get_value()
        barrel_temp_real["barrel_temp4_real"]  = {"value":barrel_temp4_real,"edit":"none"}
        barrel_temp5_real                      = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx1OqjgNGGI7xRxhPMlZoj3NWaMgw==")).get_value()
        barrel_temp_real["barrel_temp5_real"]  = {"value":barrel_temp5_real,"edit":"none"}
        # barrel_temp6_real                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx2OqjgNGGI7xRxhPMlZoj3NWaMgw==").get_value()
        # barrel_temp_real["barrel_temp6_real"]  = {"value":barrel_temp6_real,"edit":"none"}
        # barrel_temp7_real                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx3OqjgNGGI7xRxhPMlZoj3NWaMgw==").get_value()
        # barrel_temp_real["barrel_temp7_real"]  = {"value":barrel_temp7_real,"edit":"none"} 
        # barrel_temp8_real                      = self.worker.get_node("ns=8;b=AQAAAKbhKnGK9zM6oM4NS6TGE0ug7TRxm+Uhd4zXOWSMrQl6g+YjYIDsLkGH6jRnx8oufozgNH2G7RV6gPcfJcfXJXmZ5jJ1nfYycbPsLnGarRRxhPMlZoj3NWaM2S96jNx4OqjgNGGI7xRxhPMlZoj3NWaMgw==").get_value()
        # barrel_temp_real["barrel_temp8_real"]  = {"value":barrel_temp8_real,"edit":"none"} 

        self.machinestatus["barrel_temp_real"] = barrel_temp_real

        #Clamp force set
        clamp_force_set                        = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmblmG7yRXheItZIfkBnub4CU6pOwscKrvIXmZ7SdShvEjcek=")).get_value()
        self.machinestatus["clamp_force_set"]  = {"value":clamp_force_set,"edit":"none"}

        #Holding pressure & position setting
        holdingtimeset = {}
        holding_time1_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJcfCI2C96i1x6Q==")).get_value()
        holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"none"}
        holding_time2_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJsfCI2C96i1x6Q==")).get_value()
        holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"none"}
        holding_time3_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJ8fCI2C96i1x6Q==")).get_value()
        holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"none"}
        holding_time4_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIMfCI2C96i1x6Q==")).get_value()
        holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"none"}
        holding_time5_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIcfCI2C96i1x6Q==")).get_value()
        holdingtimeset["holding_time5_set"]     = {"value":holding_time5_set,"edit":"none"}
        self.machinestatus["holdingtimeset"]    = holdingtimeset
        holdingpressureset ={}
        holding_pressure1_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJcfTMnGa8DVmjIM=")).get_value()
        holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"none"}
        holding_pressure2_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJsfTMnGa8DVmjIM=")).get_value()
        holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"none"}
        holding_pressure3_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfJ8fTMnGa8DVmjIM=")).get_value()
        holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"none"}
        holding_pressure4_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIMfTMnGa8DVmjIM=")).get_value()
        holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"none"}
        holding_pressure5_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itCHuF5yl6jq0Ie4XnKXqO0DR1juYfIcfTMnGa8DVmjIM=")).get_value()
        holdingpressureset["holding_pressure5_set"] = {"value":holding_pressure5_set,"edit":"none"}
        self.machinestatus["holdingpressureset"]    = holdingpressureset
        #Injection volume(position) set
        injection_pos ={}
        injection_volume1                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume1"]     = {"value":injection_volume1,"edit":"none"}
        injection_volume2                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"none"}
        injection_volume3                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"none"}
        injection_volume4                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"none"}
        injection_volume5                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"none"}
        injection_volume6                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfTL2eA9yl7h4M=")).get_value()
        injection_pos["injection_volume6"]     = {"value":injection_volume6,"edit":"none"}
        self.machinestatus["injection_pos"]    = injection_pos
        #Injection rate(speed) set
        injection_speed = {}
        injection_rate1_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfQMHGM50A=")).get_value()
        injection_speed["injection_rate1_set"]   = {"value":injection_rate1_set,"edit":"none"}
        injection_rate2_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfQMHGM50A=")).get_value()
        injection_speed["injection_rate2_set"]   = {"value":injection_rate2_set,"edit":"none"}
        injection_rate3_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fQMHGM50A=")).get_value()
        injection_speed["injection_rate3_set"]   = {"value":injection_rate3_set,"edit":"none"}
        injection_rate4_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfQMHGM50A=")).get_value()
        injection_speed["injection_rate4_set"]   = {"value":injection_rate4_set,"edit":"none"}
        injection_rate5_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfQMHGM50A=")).get_value()
        injection_speed["injection_rate5_set"]   = {"value":injection_rate5_set,"edit":"none"}
        injection_rate6_set                      = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfQMHGM50A=")).get_value()
        injection_speed["injection_rate6_set"]   = {"value":injection_rate6_set,"edit":"none"}
        self.machinestatus["injection_speed"]    = injection_speed
        #Cooling time
        cooling_time                          = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itA3uG7yl6jtcpeYyD")).get_value()
        self.machinestatus["cooling_time"]    = {"value":cooling_time,"edit":"none"}
        #VP position setting
        vp_position_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo6tBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo7TL2eA9yl7h4M=")).get_value()
        self.machinestatus["vp_position_set"] = {"value":vp_position_set,"edit":"none"}
        #Filling Time Limit Setting
        filling_time_limit_set                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo6tBn2F7yl6jtA3fZ3gKH2H5Ah7hecpeo7XKXmMgw==")).get_value()
        self.machinestatus["filling_time_set"] = {"value":filling_time_limit_set,"edit":"none"}

        #Injection pressure setting
        injection_pressure_list                            = {}
        injection_pressure1_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJcfTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure1_set"] = {"value":injection_pressure1_set,"edit":"none"}
        injection_pressure2_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJsfTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure2_set"] = {"value":injection_pressure2_set,"edit":"none"}
        injection_pressure3_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfJ8fTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure3_set"] = {"value":injection_pressure3_set,"edit":"none"}
        injection_pressure4_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIMfTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure4_set"] = {"value":injection_pressure4_set,"edit":"none"}
        injection_pressure5_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIcfTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure5_set"] = {"value":injection_pressure5_set,"edit":"none"}
        injection_pressure6_set                            = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBn2F7yl6jq0GfYXvKXqO0DR1juYfIsfTMnGa8DVmjIM=")).get_value()
        injection_pressure_list["injection_pressure6_set"] = {"value":injection_pressure6_set,"edit":"none"}
        self.machinestatus["injection_pressure_list"]      = injection_pressure_list

        #Back pressure
        backpressure  = {}
        backpressure1                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrJuRJvmM2ec8SUU")).get_value()
        backpressure["backpressure1"]       = {"value":backpressure1,"edit":"none"}
        backpressure2                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrFuRJvmM2ec8SUU")).get_value()
        backpressure["backpressure2"]       = {"value":backpressure2,"edit":"none"}
        backpressure3                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrBuRJvmM2ec8SUU")).get_value()
        backpressure["backpressure3"]       = {"value":backpressure3,"edit":"none"}
        backpressure4                       = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrduRJvmM2ec8SUU")).get_value()
        backpressure["backpressure4"]       = {"value":backpressure4,"edit":"none"}
        self.machinestatus["backpressure"]  = backpressure
        # Dosing position 
        Dospos = {}
        dos_position1                 = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrJuRJvmM2ec8SUU")).get_value()
        Dospos["dos_position1"]       = {"value":dos_position1,"edit":"none"}
        dos_position2                 = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrFuRIbwKWCA7C4U")).get_value()
        Dospos["dos_position2"]       = {"value":dos_position2,"edit":"none"}
        dos_position3                 = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrBuRIbwKWCA7C4U")).get_value()
        Dospos["dos_position3"]       = {"value":dos_position3,"edit":"none"}
        dos_position4                 = self.worker.get_node(self.get_node_safe("ns=11;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuHzi94jeouc7niMnWE5jRxm/AUbZnmbl2H6SV3neoverztKWC65jRggO0nS9itBHua6i5zx8cvZ4DtJ0ed4idxtrduRIbwKWCA7C4U")).get_value()
        Dospos["dos_position4"]       = {"value":dos_position4,"edit":"none"}
        self.machinestatus["Dospos"]  = Dospos
        # FEED BACK 
        #Act cycle time
        act_cycle_time                         = self.worker.get_node(self.get_node_safe("ns=9;b=AQAAAKbhKnGK9zM6qvojeIzTIWaI7iVgjPEzUZ/mLmC9+jBxx8A5d4XmFH2E5kA=")).get_value()
        self.machinefeedback["act_cycle_time"] = act_cycle_time
        #VP position real
        vp_position_real                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHH1RBXgeIuc4zMNnGb0y9ngPcpe4eD")).get_value()
        self.machinefeedback["vp_position_real"] = vp_position_real
        # Filling time
        filling_time                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHHyi5+jOA0fYbtFH2E5kA=")).get_value()
        self.machinefeedback["filling_time"] = filling_time
        # Material Cushion (餘料)
        material_cushion                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHHwDVngeoverr3MnuC5kA=")).get_value()
        self.machinefeedback["material_cushion"] = material_cushion
        # Maximun real injection pressure (SpecificPressure)
        Maximun_real_injection_pressure                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHH0DBxiuomfYrTMnGa8DVmjM4hbIDuNXnp")).get_value()
        self.machinefeedback["Maximun_real_injection_pressure"] = Maximun_real_injection_pressure
        # Filling start position
        filling_start_position                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHHyi5+jOA0fYbtE2CI8TREhvApYIDsLhQ=")).get_value()
        self.machinefeedback["filling_start_position"] = filling_start_position
        # Maximun real Holding pressure (SpecificPressure)
        Maximun_real_holding_pressure                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHHyy94jdAwcYrqJn2K0zJxmvA1ZozOIWyA7jV56Q==")).get_value()
        self.machinefeedback["Maximun_real_holding_pressure"] = Maximun_real_holding_pressure
        # Act plastic time
        act_plastic_time                         = self.worker.get_node(self.get_node_safe("ns=8;b=AQAAAKbhKnGK9zM6oO0qcYr3KXuH1i59ncA5d4XmEHWb4i1xneYyZ736MHHHxy9ngO0nQIDuJRQ=")).get_value()
        self.machinefeedback["act_plastic_time"] = act_plastic_time
  

        if processstatus != 5:
            self.machinestatus['machine'] = {"value":"work","edit":"none"}
            self.processactivate=True
        else:
            self.machinestatus['machine'] = {"value":"stay","edit":"none"}
            if self.processactivate == True:
                print("[Message] Save data ...")
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
    machineaddress = '192.168.1.10:4840'
    Tachung          = tachungagent(machineaddress,'Tachung')
    Tachung.connect()
    import time
    Tachung.parametersetting("holding_time1_set","79")
    while True:
      try:
        Tachung.collectdata()
        with open("healthcheck.txt", "w+") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      except Exception as e:
          print(e)    




