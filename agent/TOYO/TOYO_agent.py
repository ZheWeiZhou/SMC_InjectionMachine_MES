from pprint import pprint
import os
import json
import time
import redis
from datetime import datetime
from sqlalchemy import create_engine,text, Column, Integer, String,DateTime,TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
import pika
Base = declarative_base()
class injection_machine_db(Base):
    __tablename__    = "MachineHistory"
    id               = Column(Integer, primary_key=True)
    created_at       = Column(TIMESTAMP)
    machine_name     = Column(TEXT)
    machine_status   = Column(TEXT)
    machine_feedback = Column(TEXT)
    machine_curve    = Column(TEXT)
class toyoagent:
    def __init__(self,spc_path,machineid):
        self.rabbitmq_account = "cax"
        self.rabbitmq_password = "cax521"
        self.machineid = machineid
        self.previous_count = -1
        self.spc_path       = spc_path
        self.hostip = "192.168.1.50"
        self.red = redis.Redis(host='192.168.1.50',port=6379,db=0)
        self.db=create_engine("postgresql://postgres:postgres@192.168.1.50:5432/cax")
        self.machineupdatetime = ''
        self.nodemap ={
            "Ijv_set1":"@SetVelInj_V_0[1]",
            "Ijv_set2":"@SetVelInj_V_1[1]",
            "Ijv_set3":"@SetVelInj_V_2[1]",
            "Ijv_set4":"@SetVelInj_V_3[1]",
            "Ijv_set5":"@SetVelInj_V_4[1]",
            "Ijv_set6":"@SetVelInj_V_5[1]",
            "Ijv_set7":"@SetVelInj_V_6[1]",
            "injection_pressure_set":"SetPrsXfrSpec[1]",
            "VP_pos_set":"@SetStrInj_S_10[1]",
            "IJ_pos_set0":"SetStrPlst[1]",
            "IJ_pos_set1":"@SetStrInj_S_1[1]",
            "IJ_pos_set2":"@SetStrInj_S_2[1]",
            "IJ_pos_set3":"@SetStrInj_S_3[1]",
            "IJ_pos_set4":"@SetStrInj_S_4[1]",
            "IJ_pos_set5":"@SetStrInj_S_5[1]",
            "IJ_pos_set6":"@SetStrInj_S_6[1]",
            "Barrel_temp_set1":"SetTmpBrlZn[1,1]",
            "Barrel_temp_set2":"SetTmpBrlZn[1,2]",
            "Barrel_temp_set3":"SetTmpBrlZn[1,3]",
            "Barrel_temp_set4":"SetTmpBrlZn[1,4]",
            "Barrel_temp_set5":"SetTmpBrlZn[1,5]",
            "Barrel_temp_set6":"SetTmpBrlZn[1,6]",
            "clamp_force_set":"SetFrcClp",
            "cooling_time":"@SetTimCnt_CoolTim",
            "Holding_time_set1":"@SetTimHld_T_1[1]",
            "Holding_time_set2":"@SetTimHld_T_2[1]",
            "Holding_time_set3":"@SetTimHld_T_3[1]",
            "Holding_time_set4":"@SetTimHld_T_4[1]",
            "Holding_time_set5":"@SetTimHld_T_5[1]",
            "Holding_time_set6":"@SetTimHld_T_6[1]",
            "Holding_pressure_set1":"@SetPrsInj_P_1[1]",
            "Holding_pressure_set2":"@SetPrsInj_P_2[1]",
            "Holding_pressure_set3":"@SetPrsInj_P_3[1]",
            "Holding_pressure_set4":"@SetPrsInj_P_4[1]",
            "Holding_pressure_set5":"@SetPrsInj_P_5[1]",
            "Holding_pressure_set6":"@SetPrsInj_P_6[1]",
            "filling_time_set":"@SetTimInj_T_0[1]",
            "backpressure1":"@SetPrsPlst_Pc_0[1]",
            "backpressure2":"@SetPrsPlst_Pc_1[1]",
            "backpressure3":"@SetPrsPlst_Pc_2[1]"
        }
    def send_monitor_command(self):
        os.system('copy "SESS0000.REQ" "Session\SESS0000.REQ"')
        def callback(ch, method, properties, body):
                command = json.loads(body.decode())
                if 'Batch' in command:
                    self.batchparametersetting(command["Target"],command["Value"])
                else:
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
    def get_machine_data(self):
        data = {
                    "date":'',
                    "time":'',
                    "Actmach":'',
                    "Ijv_set1":'',
                    "Ijv_set2":'',
                    "Ijv_set3":'',
                    "Ijv_set4":'',
                    "Ijv_set5":'',
                    "Ijv_set6":'',
                    "Ijv_set7":'',
                    "VP_pos_set":'',
                    "Act_VP_pressure":'',
                    "Act_VP_pos":'',
                    "Act_filling_time":'',
                    "IJ_pos_set1":'',
                    "IJ_pos_set2":'',
                    "IJ_pos_set3":'',
                    "IJ_pos_set4":'',
                    "IJ_pos_set5":'',
                    "IJ_pos_set6":'',
                    "Barrel_temp_set1":'',
                    "Barrel_temp_set2":'',
                    "Barrel_temp_set3":'',
                    "Barrel_temp_set4":'',
                    "Barrel_temp_set5":'',
                    "Barrel_temp_set6":'',
                    "Act_Barrel_temp1":'',
                    "Act_Barrel_temp2":'',
                    "Act_Barrel_temp3":'',
                    "Act_Barrel_temp4":'',
                    "Act_Barrel_temp5":'',
                    "Act_Barrel_temp6":'',
                    "Act_Cushion_pos":'',
                    "Ij_pos_set0":'',
                    "clamp_force_set":'',
                    "cooling_time":'',
                    "Max_ij_pressure":'',
                    "Max_ij_speed":'',
                    "Holding_time_set1":'',
                    "Holding_time_set2":'',
                    "Holding_time_set3":'',
                    "Holding_time_set4":'',
                    "Holding_time_set5":'',
                    "Holding_time_set6":'',
                    "Holding_pressure_set1":'',
                    "Holding_pressure_set2":'',
                    "Holding_pressure_set3":'',
                    "Holding_pressure_set4":'',
                    "Holding_pressure_set5":'',
                    "Holding_pressure_set6":'',
                    "Act_ij_speed1":'',
                    "Act_ij_speed2":'',
                    "Act_ij_speed3":'',
                    "Act_ij_speed4":'',
                    "Act_ij_speed5":'',
                    "Act_ij_speed6":'',
                    "Act_ij_speed7":'',
                    "Act_ij_pressure1":'',
                    "Act_ij_pressure2":'',
                    "Act_ij_pressure3":'',
                    "Act_ij_pressure4":'',
                    "Act_ij_pressure5":'',
                    "Act_ij_pressure6":'',
                    "Act_ij_pressure7":'',
                    "Min_ij_pressure":'',
                    "Min_ij_speed":'',
                    "cycle_count":'',
                    "filling_time_set":'',
                    "PostionSeg":'',
                    "injection_pressure_set":'',
                    "backpressure1":'',
                    "backpressure2":'',
                    "backpressure3":'',
                    "backpressureseg":''
                }
        try:
            content = 0
            with open(self.spc_path,'r') as file:
                content     = file.readlines()
                lastline    = content[-1].strip()
                machinedata = [s.strip() for s in lastline.split(',') ]
                keylist  = list(data.keys())
                for i in range(len(machinedata)):
                    try:
                        keyname       = keylist[i]
                        data[keyname] = machinedata[i]
                    except :
                        pass
                    


            data["IJ_pos_set1"] = data["IJ_pos_set1"] if float(data["PostionSeg"]) > 1 else -1
            data["IJ_pos_set2"] = data["IJ_pos_set2"] if float(data["PostionSeg"]) > 2 else -1
            data["IJ_pos_set3"] = data["IJ_pos_set3"] if float(data["PostionSeg"]) > 3 else -1
            data["IJ_pos_set4"] = data["IJ_pos_set4"] if float(data["PostionSeg"]) > 4 else -1
            data["IJ_pos_set5"] = data["IJ_pos_set5"] if float(data["PostionSeg"]) > 5 else -1
            data["IJ_pos_set6"] = data["IJ_pos_set6"] if float(data["PostionSeg"]) > 6 else -1


            data["Ijv_set2"] = data["Ijv_set2"] if float(data["PostionSeg"]) > 1 else -1
            data["Ijv_set3"] = data["Ijv_set3"] if float(data["PostionSeg"]) > 2 else -1
            data["Ijv_set4"] = data["Ijv_set4"] if float(data["PostionSeg"]) > 3 else -1
            data["Ijv_set5"] = data["Ijv_set5"] if float(data["PostionSeg"]) > 4 else -1
            data["Ijv_set6"] = data["Ijv_set6"] if float(data["PostionSeg"]) > 5 else -1
            data["Ijv_set7"] = data["Ijv_set7"] if float(data["PostionSeg"]) > 6 else -1

            data["backpressure2"] = data["backpressure2"] if float(data["backpressureseg"]) > 1 else -1
            data["backpressure3"] = data["backpressure3"] if float(data["backpressureseg"]) > 2 else -1


            # data["injection_pressure2_set"] = data["injection_pressure2_set"] if float(data["PostionSeg"]) > 1 else -1
            # data["injection_pressure3_set"] = data["injection_pressure3_set"] if float(data["PostionSeg"]) > 2 else -1
            # data["injection_pressure4_set"] = data["injection_pressure4_set"] if float(data["PostionSeg"]) > 3 else -1
            # data["injection_pressure5_set"] = data["injection_pressure5_set"] if float(data["PostionSeg"]) > 4 else -1
            # data["injection_pressure6_set"] = data["injection_pressure6_set"] if float(data["PostionSeg"]) > 5 else -1
            # data["injection_pressure7_set"] = data["injection_pressure7_set"] if float(data["PostionSeg"]) > 6 else -1


            # Clean spc.dat per hour
            if len(content) > 3600:
                print("[Message] Detect SPC file row number exceed maximunm limit")
                os.remove(self.spc_path)
                time.sleep(2)
        except Exception as e:
            print(f"[Error] Get Data Fail Reason : {e}")
            pass
        return data
    
    # 響應Rabbit MQ的task更改機台參數
    def parametersetting(self,target,value):
        access_node = list(self.nodemap.keys())
        print(target)
        if target in access_node:
            nodeid = self.nodemap[target]
            print(nodeid)
            with open('SET.JOB','r') as file:
                first_line  = file.readline()
            with open('SET.JOB','w') as file:
                file.write(first_line)
            # CREATE NEW SET JOB
            with open('SET.JOB','a') as file:
                new_line = f"SET {nodeid} {value}\n"
                file.write(new_line)
            # Send command
            setlog_path = 'data\SET.log'
            if os.path.exists(setlog_path):
                os.remove('data\SET.log')
            os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')
    def batchparametersetting(self,target,value):
        access_node = list(self.nodemap.keys())
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)   
        with open('SET.JOB','a') as file:
            for i in range(len(target)):
                 targetname = target[i]
                 if targetname in access_node:
                    nodeid    = self.nodemap[targetname]
                    setvalue  = value[i]
                    new_line  = f"SET {nodeid} {setvalue}\n"
                    file.write(new_line)
            setlog_path = 'data\SET.log'
            if os.path.exists(setlog_path):
                os.remove('data\SET.log')
            os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

                
    def set_injection_pos(self,pos):
        '''
        SetStrPlst[1]
        @SetStrInj_S_1[1],
        @SetStrInj_S_2[1],
        @SetStrInj_S_3[1],
        @SetStrInj_S_4[1],
        @SetStrInj_S_5[1],
        @SetStrInj_S_6[1],
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(pos)):
                if i == 0:
                    new_line = f"SET SetStrPlst[1] {pos[i]}\n"
                else:
                    new_line = f"SET @SetStrInj_S_{i}[1] {pos[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

    def set_injection_speed(self,speed):
        '''
            @SetVelInj_V_0[1],
            @SetVelInj_V_1[1],
            @SetVelInj_V_2[1],
            @SetVelInj_V_3[1],
            @SetVelInj_V_4[1],
            @SetVelInj_V_5[1],
            @SetVelInj_V_6[1],
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(speed)):
                new_line = f"SET @SetVelInj_V_{i}[1] {speed[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')
        
    def set_barrel_temp(self,temp):
        '''
            SetTmpBrlZn[1,1],
            SetTmpBrlZn[1,2],
            SetTmpBrlZn[1,3],
            SetTmpBrlZn[1,4],
            SetTmpBrlZn[1,5],
            SetTmpBrlZn[1,6],
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(temp)):
                new_line = f"SET SetTmpBrlZn[1,{i+1}] {temp[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

    def set_holding_pressure(self,holdingpressure):
        '''
                @SetPrsInj_P_1[1],
                @SetPrsInj_P_2[1],
                @SetPrsInj_P_3[1],
                @SetPrsInj_P_4[1],
                @SetPrsInj_P_5[1],
                @SetPrsInj_P_6[1],
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(holdingpressure)):
                new_line = f"SET @SetPrsInj_P_{i+1}[1] {holdingpressure[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

    def set_holding_time(self,holdingtime):
        '''
            @SetTimHld_T_1[1],
            @SetTimHld_T_2[1],
            @SetTimHld_T_3[1],
            @SetTimHld_T_4[1],
            @SetTimHld_T_5[1],
            @SetTimHld_T_6[1],
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(holdingtime)):
                new_line = f"SET @SetTimHld_T_{i+1}[1] {holdingtime[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"') 

    def set_cooling_time(self,coolingtime):
        '''
            @SetTimCnt_CoolTim
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(coolingtime)):
                new_line = f"SET @SetTimCnt_CoolTim {coolingtime[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

    def set_injection_pressure(self,ijpressure):
        '''
            @SetPrsInj_P_9[1]
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(ijpressure)):
                new_line = f"SET @SetPrsInj_P_9[1] {ijpressure[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')

    def set_vp_pos(self,vppos):
        '''
            @SetPrsInj_P_9[1]
        '''
        # Reset SET.JOB
        with open('SET.JOB','r') as file:
            first_line  = file.readline()
        with open('SET.JOB','w') as file:
            file.write(first_line)
        # Create New SET.JOB
        with open('SET.JOB','a') as file:
            for i in range(len(vppos)):
                new_line = f"SET @SetStrInj_S_10[1] {vppos[i]}\n"
                file.write(new_line)
        # Send command
        setlog_path = 'data\SET.log'
        if os.path.exists(setlog_path):
            os.remove('data\SET.log')
        os.system('copy "SESS0001.REQ" "Session\SESS0001.REQ"')  

    def collectdata(self):

        machinedata = self.get_machine_data()
        # pprint(machinedata)
        # for i in list(machinedata.keys()):
        #     print(f"{i}: {machinedata[i]}")

        try:
            currentcount = int(machinedata['cycle_count'])
            # upload machine real-time data to redis
            print("[Message] Upload realtime data to redis ... ")

            current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.red.set(f'{self.machineid}_updatetime',current_time)

            statusdata = {}
            injection_speed = {}
            injection_speed["Ijv_set1"]       = {"value":machinedata["Ijv_set1"],"edit":"acctivate"}
            injection_speed["Ijv_set2"]       = {"value":machinedata["Ijv_set2"],"edit":"acctivate"}
            injection_speed["Ijv_set3"]       = {"value":machinedata["Ijv_set3"],"edit":"acctivate"}
            injection_speed["Ijv_set4"]       = {"value":machinedata["Ijv_set4"],"edit":"acctivate"}
            injection_speed["Ijv_set5"]       = {"value":machinedata["Ijv_set5"],"edit":"acctivate"}
            injection_speed["Ijv_set6"]       = {"value":machinedata["Ijv_set6"],"edit":"acctivate"}
            injection_speed["Ijv_set7"]       = {"value":machinedata["Ijv_set7"],"edit":"acctivate"}
            statusdata["injection_speed"]     = injection_speed

            # statusdata["injection_pressure_set"] = {"value":machinedata["injection_pressure_set"],"edit":"acctivate"}
            statusdata["VP_pos_set"]     = {"value":machinedata["VP_pos_set"],"edit":"acctivate"}
            injection_pos ={}
            injection_pos["Ij_pos_set0"]    = {"value":machinedata["Ij_pos_set0"],"edit":"none"}
            injection_pos["IJ_pos_set1"]    = {"value":machinedata["IJ_pos_set1"],"edit":"acctivate"}
            injection_pos["IJ_pos_set2"]    = {"value":machinedata["IJ_pos_set2"],"edit":"acctivate"}
            injection_pos["IJ_pos_set3"]    = {"value":machinedata["IJ_pos_set3"],"edit":"acctivate"}
            injection_pos["IJ_pos_set4"]    = {"value":machinedata["IJ_pos_set4"],"edit":"acctivate"}
            injection_pos["IJ_pos_set5"]    = {"value":machinedata["IJ_pos_set5"],"edit":"acctivate"}
            injection_pos["IJ_pos_set6"]    = {"value":machinedata["IJ_pos_set6"],"edit":"acctivate"}
            statusdata["injection_pos"]     = injection_pos
            barrel_temp_set = {}
            barrel_temp_set["Barrel_temp_set1"]   = {"value":machinedata["Barrel_temp_set1"],"edit":"acctivate"}
            barrel_temp_set["Barrel_temp_set2"]   = {"value":machinedata["Barrel_temp_set2"],"edit":"acctivate"}
            barrel_temp_set["Barrel_temp_set3"]   = {"value":machinedata["Barrel_temp_set3"],"edit":"acctivate"}
            barrel_temp_set["Barrel_temp_set4"]   = {"value":machinedata["Barrel_temp_set4"],"edit":"acctivate"}
            barrel_temp_set["Barrel_temp_set5"]   = {"value":machinedata["Barrel_temp_set5"],"edit":"acctivate"}
            barrel_temp_set["Barrel_temp_set6"]   = {"value":machinedata["Barrel_temp_set6"],"edit":"acctivate"}
            statusdata["barrel_temp_set"]         = barrel_temp_set
            
            barrel_temp_real = {}
            barrel_temp_real["Act_Barrel_temp1"] = {"value":machinedata["Act_Barrel_temp1"],"edit":"none"}
            barrel_temp_real["Act_Barrel_temp2"] = {"value":machinedata["Act_Barrel_temp2"],"edit":"none"}
            barrel_temp_real["Act_Barrel_temp3"] = {"value":machinedata["Act_Barrel_temp3"],"edit":"none"}
            barrel_temp_real["Act_Barrel_temp4"] = {"value":machinedata["Act_Barrel_temp4"],"edit":"none"}
            barrel_temp_real["Act_Barrel_temp5"] = {"value":machinedata["Act_Barrel_temp5"],"edit":"none"}
            barrel_temp_real["Act_Barrel_temp6"] = {"value":machinedata["Act_Barrel_temp6"],"edit":"none"}
            statusdata["barrel_temp_real"]       = barrel_temp_real

            statusdata["clamp_force_set"] = {"value":machinedata["clamp_force_set"],"edit":"acctivate"}
            statusdata["cooling_time"]   = {"value":machinedata["cooling_time"],"edit":"acctivate"}
            holdingtimeset = {}
            holdingtimeset["Holding_time_set1"]  = {"value":machinedata["Holding_time_set1"],"edit":"acctivate"}
            holdingtimeset["Holding_time_set2"]  = {"value":machinedata["Holding_time_set2"],"edit":"acctivate"}
            holdingtimeset["Holding_time_set3"]  = {"value":machinedata["Holding_time_set3"],"edit":"acctivate"}
            holdingtimeset["Holding_time_set4"]  = {"value":machinedata["Holding_time_set4"],"edit":"acctivate"}
            holdingtimeset["Holding_time_set5"]  = {"value":machinedata["Holding_time_set5"],"edit":"acctivate"}
            holdingtimeset["Holding_time_set6"]  = {"value":machinedata["Holding_time_set6"],"edit":"acctivate"}
            statusdata["holdingtimeset"]         = holdingtimeset

            holdingpressureset ={}
            holdingpressureset["Holding_pressure_set1"] = {"value":machinedata["Holding_pressure_set1"],"edit":"acctivate"}
            holdingpressureset["Holding_pressure_set2"] = {"value":machinedata["Holding_pressure_set2"],"edit":"acctivate"}
            holdingpressureset["Holding_pressure_set3"] = {"value":machinedata["Holding_pressure_set3"],"edit":"acctivate"}
            holdingpressureset["Holding_pressure_set4"] = {"value":machinedata["Holding_pressure_set4"],"edit":"acctivate"}
            holdingpressureset["Holding_pressure_set5"] = {"value":machinedata["Holding_pressure_set5"],"edit":"acctivate"}
            holdingpressureset["Holding_pressure_set6"] = {"value":machinedata["Holding_pressure_set6"],"edit":"acctivate"}
            statusdata["holdingpressureset"]            = holdingpressureset

            statusdata["filling_time_set"]            = {"value":machinedata["filling_time_set"],"edit":"acctivate"}
            statusdata["injection_pressure_set"]      = {"value":machinedata["injection_pressure_set"],"edit":"acctivate"}
            backpressure  = {}
            backpressure["backpressure1"]       = {"value":machinedata["backpressure1"],"edit":"acctivate"}
            backpressure["backpressure2"]       = {"value":machinedata["backpressure2"],"edit":"acctivate"}
            backpressure["backpressure3"]       = {"value":machinedata["backpressure3"],"edit":"acctivate"}
            statusdata["backpressure"] = backpressure
            self.red.set(f'{self.machineid}_status',json.dumps(statusdata))

            feedbackdata ={}
            feedbackdata["Act_VP_pressure"] = machinedata["Act_VP_pressure"]
            feedbackdata["Act_VP_pos"] = machinedata["Act_VP_pos"]
            feedbackdata["Act_filling_time"] = machinedata["Act_filling_time"]
            feedbackdata["Act_Cushion_pos"] = machinedata["Act_Cushion_pos"]
            feedbackdata["Max_ij_pressure"] = machinedata["Max_ij_pressure"]
            feedbackdata["Max_ij_speed"] = machinedata["Max_ij_speed"]
            feedbackdata["Min_ij_pressure"] = machinedata["Min_ij_pressure"]
            feedbackdata["Min_ij_speed"] = machinedata["Min_ij_speed"]
            self.red.set(f'{self.machineid}_feedback',json.dumps(feedbackdata))
            actpressure = [machinedata["Act_ij_pressure1"],machinedata["Act_ij_pressure2"],machinedata["Act_ij_pressure3"],machinedata["Act_ij_pressure4"],machinedata["Act_ij_pressure5"],machinedata["Act_ij_pressure6"],machinedata["Act_ij_pressure7"]]
            actspeed = [machinedata["Act_ij_speed1"],machinedata["Act_ij_speed2"],machinedata["Act_ij_speed3"],machinedata["Act_ij_speed4"],machinedata["Act_ij_speed5"],machinedata["Act_ij_speed6"],machinedata["Act_ij_speed7"]]
            curvedata = {}
            curvedata["actpressure"] = actpressure
            curvedata["actspeed"]    = actspeed
            self.red.set(f'{self.machineid}_curve',json.dumps(curvedata))


            
            if self.previous_count < 0:
                self.previous_count = int(machinedata['cycle_count'])
            else:
                # Determine whether data needs to be uploaded to the database.
                if self.previous_count != currentcount:
                    print("[Message] Detect machine completed the process, Start to upload data to db ... ")
                    current_time = datetime.now().strftime("%Y-%m-%d")
                    current_time = current_time + ' ' +  machinedata["time"]
                    Session = sessionmaker(bind=self.db)
                    session = Session()
                    insert_sql = injection_machine_db.__table__.insert().values(
                        created_at       = current_time,
                        machine_name     = self.machineid,
                        machine_status   = json.dumps(statusdata),
                        machine_feedback = json.dumps(feedbackdata),
                        machine_curve    = json.dumps(curvedata)
                    )
                    session.execute(insert_sql)
                    session.commit()
                    session.close()
                    self.previous_count=currentcount
        except Exception as e:
            print(f"[Error] Collect data process crash ... Reason {e}")
            pass
            
if __name__ == "__main__":
    agent       = toyoagent('data/spc.dat','TOYO')
    agent.send_monitor_command()
    # agent.set_injection_pos([105.00,27.00])
    # agent.set_injection_speed([100.0,100.0])
    while True:
        agent.collectdata()
        time.sleep(1)
