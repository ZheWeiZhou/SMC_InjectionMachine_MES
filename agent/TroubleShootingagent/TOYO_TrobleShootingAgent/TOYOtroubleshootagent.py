import redis
import TOYO_dataprocess_function as dp
import json
import time
import requests
import copy
import pika
import threading
from datetime import datetime,timezone
class TOYOtroubleshootagent:
    def __init__(self,hostip,machinename):
        self.hostip = hostip
        self.red = redis.Redis(host=self.hostip,port=6379,db=0)
        self.activatesignal = False
        self.rabbitmq_account = "cax"
        self.rabbitmq_pass = "cax521"
        self.machine_name = machinename
        self.adjustabstract = []
    def connect(self):  
        try:
            def callback(ch, method, properties, body):
                command = json.loads(body.decode())
                DeffectLevel = int(command["DeffectLevel"])
                self.autocheck(command["Deffect"],DeffectLevel)
            def start_controller():
                while True:
                    try:
                        connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=self.hostip,
                            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
                        ))
                        channel = connection.channel()
                        channel.queue_declare(queue=f"{self.machine_name}_troubleshooting")
                        channel.basic_consume(queue=f"{self.machine_name}_troubleshooting",
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
            print("[ERROR] Connect to Rabbit MQ fail")
    # 如果診斷出劑量過少的解決方法
    def slovelowdose(self,machinestatus,machinefeedback,deffectlevel):
        vpsetting       = machinestatus["VP_pos_set"]
        ijpos_set       = machinestatus["injection_pos"]
        ijpos_set_key   = list(ijpos_set.keys())
        ijpose_set_list = []
        for key in ijpos_set_key:
            positem = ijpos_set[key]["value"]
            if positem >= 0:
                ijpose_set_list.append(positem)
        actijvolume   = max(ijpose_set_list) - vpsetting
        # 根據缺陷嚴重程度決定參數調整幅度
        adjustratio   = 1.05
        if deffectlevel == 2:
            adjustratio   = 1.2
        if deffectlevel == 3:
             adjustratio   = 1.3
        if deffectlevel == 4:
             adjustratio   = 1.35        
        newvolume =  actijvolume * adjustratio
        lastpos   =  max(ijpose_set_list) - newvolume 
        newijpos_set = copy.deepcopy(ijpose_set_list)
        # 如果發現直接調整最後的射出位置劑量還是不夠...
        if lastpos < 0 :
            newijpos_set[0]  = newijpos_set[0] + lastpos*-1
            newijpos_set[-1] = newijpos_set[0] - newvolume
        else:
            newijpos_set[-1] = newijpos_set[0] - newvolume
        # 最後再檢查預留給保壓的劑量夠不夠
        holdingdoseprecent = newijpos_set[-1] / newvolume
        if holdingdoseprecent < 0.1:
            newijpos_set[0]  = newijpos_set[0] + newvolume *0.1
            newijpos_set[-1] = newijpos_set[0] - newvolume 
        # 計算出新的射出位置之後，透過agent回寫參數
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.machine_name)
        for i in range(len(newijpos_set)):
            target = f"injection_volume{i+1}"
            value  = newijpos_set[i]
            commandbody = {"Target":target,"Value":value}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                        routing_key=self.machine_name,
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )
        # 同時也把VP位置也設定好
        commandbody = {"Target":"VP_pos_set","Value":newijpos_set[-1]}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
                        routing_key=self.machine_name,
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )

        # Create Adjust Abstract 
        original = str(ijpose_set_list)
        newset   = str(newijpos_set)
        abstract = {"Parameter":"Injection Position","Origin":original, "New":newset}
        self.adjustabstract.append(abstract)
    # 如果診斷出充填限制時間過短
    def sloveshortfillingtimeset(self,machinestatus,deffectlevel):
        CurrentFillingTimeSet = machinestatus["filling_time_set"]["value"]
        adjustratio   = 1.05
        if deffectlevel == 2:
            adjustratio   = 1.2
        if deffectlevel == 3:
             adjustratio   = 1.3
        if deffectlevel == 4:
             adjustratio   = 1.35  
        NewFillingTimeSet = CurrentFillingTimeSet * adjustratio
        # 計算出新的Filling Time之後，透過agent回寫參數
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.machine_name)
        target = "filling_time_set"
        value  = NewFillingTimeSet
        commandbody = {"Target":target,"Value":value}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
                        routing_key=self.machine_name,
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )
        original = str(CurrentFillingTimeSet)
        newset   = str(NewFillingTimeSet)
        abstract = {"Parameter":"Filling Time Limit","Origin":original, "New":newset}
        self.adjustabstract.append(abstract)
    # 診斷射速過低
    def slovelowspeed(self,machinestatus,deffectlevel,machinelimit):
        # 如果射速設的超級小，小到乘完係數之後變動幅度不到機台最高射速的2%，那就直接加上2%的機台最高射速來加速調機速度
        adjustratio   = 1.05
        if deffectlevel == 2:
            adjustratio   = 1.2
        if deffectlevel == 3:
             adjustratio   = 1.3
        if deffectlevel == 4:
             adjustratio   = 1.35  
        CurrentSpeedSet = machinestatus["injection_speed"]
        speed_set_key   = list(CurrentSpeedSet.keys())
        speed_set_list = []
        for key in speed_set_key:
            positem = CurrentSpeedSet[key]["value"]
            if positem >= 0:
                speed_set_list.append(positem)
        new_speed_set_list = []
        for oldspeed in speed_set_list:
            
            newspeed = oldspeed * adjustratio
            changerange = (newspeed - oldspeed)/ machinelimit
            if changerange <0.02:
                 newspeed = oldspeed + machinelimit*0.02
            if oldspeed > min(speed_set_list) *2:
                newspeed = oldspeed
            if newspeed > machinelimit:
                newspeed = machinelimit
            new_speed_set_list.append(newspeed)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.machine_name)
        for i in range(len(new_speed_set_list)):
            target = f"injection_rate{i+1}_set"
            value  = new_speed_set_list[i]
            commandbody = {"Target":target,"Value":value}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                            routing_key=self.machine_name,
                            body=commandbody,
                            #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                            )
        # Create Adjust Abstract 
        original = str(speed_set_list)
        newset   = str(new_speed_set_list)
        abstract = {"Parameter":"Injection Speed","Origin":original, "New":newset}
        self.adjustabstract.append(abstract)
    # 診斷射壓過低
    def slovelowpressure(self,machinestatus,deffectlevel,machinelimit):
        adjustratio   = 1.05
        if deffectlevel == 2:
            adjustratio   = 1.2
        if deffectlevel == 3:
             adjustratio   = 1.3
        if deffectlevel == 4:
             adjustratio   = 1.35  
        currentpressureset = machinestatus["injection_pressure_set"] 
        
        newset = currentpressureset * adjustratio
        # 檢查新設定的射壓有沒有超過機台極限
        if newset > machinelimit:
            newset = machinelimit
        # 呼叫HOST更改參數
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.machine_name)
        commandbody = {"Target":"injection_pressure_set","Value":newset}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
            routing_key=self.machine_name,
            body=commandbody,
        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
        )
        # Create Adjust Abstract 
        original = str(currentpressureset)
        newset   = str(newset)
        abstract = {"Parameter":"Injection Pressure","Origin":original, "New":newset}
        self.adjustabstract.append(abstract)
    # 診斷背壓過低
    def slovelowbackpressure(self):
        print("AAAAA")
    def autocheck(self,deffect,deffectlevel):
        if deffect == "shortshot":
            machinestatus   = self.red.get(f"{self.machine_name}_status")
            machinestatus   = json.loads(machinestatus)
            machinefeedback = self.red.get(f"{self.machine_name}_feedback")
            machinefeedback = json.loads(machinefeedback)
            evidences={
                        "InjectionDoseVsFillingTime":str(dp.compare_injectiondose_fltlimit(machinestatus["injection_pos"],machinestatus["VP_pos_set"],machinestatus["filling_time_set"]["value"],300)),
                        "ActFillingTimeVsFillingTime":str(dp.compare_flt_limit(machinefeedback["filling_time"],machinestatus["filling_time_set"]["value"])),
                        "InjectionEndVsInjectionPosition":str(dp.compare_ijpos_ijend(machinestatus["injection_pos"],machinestatus["VP_pos_set"],machinefeedback["Act_Cushion_pos"])),
                        "ActBarrelTempVsSuggestTemp":str(dp.settingmaterialtmp_vs_materialtmpsuggestion(machinestatus["barrel_temp_set"],[180,260])),
                        "BackPressureVsSuggestPressure":str(dp.check_backpressure(machinestatus["backpressure"],[1,5])),
                        "MaxInjectionPressureVsSettingPressure":str(dp.max_injection_pressure_compare_injection_pressure_setting(machinestatus["injection_pressure_set"],machinefeedback["Max_ij_pressure"])),
                        "SettingPressureVsMachineLimitPressure":str(dp.settingpressure_vs_machinelimit(machinestatus["injection_pressure_set"],1958)),
                        "SettingSpeedVsMachineLimitSpeed":str(dp.settingspeed_vs_machinelimit(machinestatus["injection_speed"],300)),
                        "MaxSpeedVsSpeedSetting":str(dp.compare_realinjection_ijspeedset(machinefeedback["Max_ij_speed"],machinestatus["injection_speed"])),
                        "HighSpeedRatio":str(dp.compare_max_ijspeed_postion(machinestatus["injection_speed"],machinestatus["injection_pos"])),
                        "ShortShot":str(1)
                    }
            url = f"http://{self.hostip}:8000/smc/injectionmachinemes/troubleshooting/diagnosis"
            requestdata = {"machine_name":self.machine_name,"evidences":evidences}
            headers = {
                        'AccessToken': '8d6d4e85-b277-4102-8ffd-defcc7b7b9f9',
                        'Content-Type': 'application/json'
            }
            response = requests.post(url,headers=headers, json=requestdata)
            resdata = response.json()
            if resdata["status"] == "success":
                DefectReason = []
                reasonscore  = []
                reasonlist   = []
                Result = resdata["Data"]
                ResultKey = list(Result.keys())
                for key in ResultKey:
                    reasonlist.append(key)
                    reasonscore.append(Result[key])
                    if Result[key] > 0.55:
                        DefectReason.append(key)
            if len(DefectReason) == 0:
                max_index = reasonscore.index(max(reasonscore))
                DefectReason.append(reasonlist[max_index])
            solution = {
                    "Short Filling Time":[lambda: self.sloveshortfillingtimeset(machinestatus,deffectlevel)],
                    "Low Injection Speed":[lambda:  self.slovelowspeed(machinestatus,deffectlevel,200)],
                    "Low Injection Pressure":[lambda: self.slovelowpressure(machinestatus,deffectlevel,140)],
                    "Low Injection Dose":[lambda: self.slovelowdose(machinestatus,machinefeedback,deffectlevel)],
                    }
            modelresulttodb =""
            for reasonitem in DefectReason:
                modelresulttodb = modelresulttodb + reasonitem + ","
                for func in solution.get(reasonitem, []):
                    func()
            # Save for Train Data 
            modelresulttodb = modelresulttodb[:-1]
            abstracttodb    = self.adjustabstract
            messagetoredis  = {"DefectReason":modelresulttodb,"SloveAbstract":self.adjustabstract}
            abstracttored   = json.dumps(messagetoredis)
            self.red.set(f"{self.machine_name}_SloveAbstract",abstracttored)
            url = f"http://{self.hostip}:8000/smc/injectionmachinemes/history/insertBayesianNetworkTrainData"
            storagerequestdata = {"machine_name":self.machine_name,"modelresult":modelresulttodb,"abstract":abstracttodb}
            headers = {
                        'AccessToken': '8d6d4e85-b277-4102-8ffd-defcc7b7b9f9',
                        'Content-Type': 'application/json'
                    }
            response = requests.post(url,headers=headers, json=storagerequestdata)
            self.adjustabstract = []        
if __name__ == "__main__":
    processlineagent = TOYOtroubleshootagent("192.168.1.50","TOYO")
    processlineagent.connect()
    while True : 
        try:
            time.sleep(1)
            with open("healthcheck.txt", "w+") as file:
                file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            print(e)
            pass