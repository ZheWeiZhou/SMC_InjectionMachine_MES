import redis
import FCS_dataprocess_function as dp
import json
import time
import requests
import copy
import pika
import threading
class fcstroubleshootagent:
    def __init__(self,hostip):
        self.hostip = hostip
        self.red = redis.Redis(host=self.hostip,port=6379,db=0)
        self.activatesignal = False
        self.rabbitmq_account = "cax"
        self.rabbitmq_pass = "cax521"
    def connect(self):  
        try:
            def callback(ch, method, properties, body):
                command = json.loads(body.decode())
                self.autocheck(command["Deffect"],command["DeffectLevel"])
            def start_controller():
                while True:
                    try:
                        connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=self.hostip,
                            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_password)
                        ))
                        channel = connection.channel()
                        channel.queue_declare(queue="FCS-150_troubleshooting")
                        channel.basic_consume(queue="FCS-150_troubleshooting",
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
    # 如果診斷出劑量過少的解決方法
    def slovelowdose(self,machinestatus,machinefeedback,deffectlevel):
        ijpos_set       = machinestatus["injection_pos"]
        ijpos_set_key   = list(ijpos_set.keys())
        ijpose_set_list = []
        for key in ijpos_set_key:
            positem = ijpos_set[key]["value"]
            if positem >= 0:
                ijpose_set_list.append(positem)
        injection_end = machinefeedback["material_cushion"]
        actijvolume   = max(ijpose_set_list) - injection_end
        # 根據缺陷嚴重程度決定參數調整幅度
        adjustratio   = 1.1
        if deffectlevel == 2:
            adjustratio   = 1.25
        if deffectlevel == 3:
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
        channel.queue_declare(queue="FCS-150")
        for i in range(len(newijpos_set)):
            target = f"injection_volume{i+1}"
            value  = newijpos_set[i]
            commandbody = {"Target":target,"Value":value}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                        routing_key="FCS-150",
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )
    # 如果診斷出充填限制時間過短
    def sloveshortfillingtimeset(self,machinestatus,deffectlevel):
        CurrentFillingTimeSet = machinestatus["filling_time_set"]["value"]
        adjustratio   = 1.1
        if deffectlevel == 2:
            adjustratio   = 1.25
        if deffectlevel == 3:
             adjustratio   = 1.35
        NewFillingTimeSet = CurrentFillingTimeSet * adjustratio
        # 計算出新的Filling Time之後，透過agent回寫參數
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue="FCS-150")
        target = "filling_time_set"
        value  = NewFillingTimeSet
        commandbody = {"Target":target,"Value":value}
        commandbody = json.dumps(commandbody)
        channel.basic_publish(exchange='',
                        routing_key="FCS-150",
                        body=commandbody,
                        #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                        )
    # 診斷射速過低
    def slovelowspeed(self,machinestatus,deffectlevel,machinelimit):
        # 如果射速設的超級小，小到乘完係數之後變動幅度不到機台最高射速的2%，那就直接加上2%的機台最高射速來加速調機速度
        adjustratio   = 1.1
        if deffectlevel == 2:
            adjustratio   = 1.25
        if deffectlevel == 3:
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
        channel.queue_declare(queue="FCS-150")
        for i in range(len(new_speed_set_list)):
            target = f"injection_rate{i+1}_set"
            value  = new_speed_set_list[i]
            commandbody = {"Target":target,"Value":value}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                            routing_key="FCS-150",
                            body=commandbody,
                            #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                            )
    # 診斷射壓過低
    def slovelowpressure(self,machinestatus,deffectlevel,machinelimit):
        adjustratio   = 1.1
        if deffectlevel == 2:
            adjustratio   = 1.25
        if deffectlevel == 3:
             adjustratio   = 1.35
        pressurelist = []
        currentpressureset = machinestatus["injection_pressure_list"] 
        currentpressureset_key = list(currentpressureset.keys())
        for key in currentpressureset_key:
            pressureitem = currentpressureset[key]["value"]
            if pressureitem >=0:
                pressurelist.append(pressureitem)
        currentset = max(pressurelist)
        newset = currentset * adjustratio
        if newset > machinelimit:
            newset = machinelimit
        newpressurelist = [newset] * len(pressurelist)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostip,
            credentials=pika.PlainCredentials(self.rabbitmq_account, self.rabbitmq_pass)
        ))
        channel = connection.channel()
        channel.queue_declare(queue="FCS-150")
        for i in range(len(newpressurelist)):
            target = f"injection_pressure{i+1}_set"
            value  = newpressurelist[i]
            commandbody = {"Target":target,"Value":value}
            commandbody = json.dumps(commandbody)
            channel.basic_publish(exchange='',
                            routing_key="FCS-150",
                            body=commandbody,
                            #   properties=pika.BasicProperties(expiration='600000') # TTL Setting task timeout 60 sec will be cancel
                            )
    # 診斷背壓過低
    def slovelowbackpressure(self):
        print("AAAAA")
    def autocheck(self,deffect,deffectlevel):
        if deffect == "shortshot":
            machinestatus   = self.red.get("FCS-150_status")
            machinestatus   = json.loads(machinestatus)
            machinefeedback = self.red.get("FCS-150_feedback")
            machinefeedback = json.loads(machinefeedback)
            evidences={
                        "InjectionDoseVsFillingTime":str(dp.compare_injectiondose_fltlimit(machinestatus["injection_pos"],machinestatus["filling_time_set"]["value"])[0]),
                        "ActFillingTimeVsFillingTime":str(dp.compare_flt_limit(machinefeedback["filling_time"],machinestatus["filling_time_set"]["value"])[0]),
                        "InjectionEndVsInjectionPosition":str(dp.compare_ijpos_ijend(machinestatus["injection_pos"],machinefeedback["material_cushion"])[0]),
                        "ActBarrelTempVsSuggestTemp":str(dp.settingmaterialtmp_vs_materialtmpsuggestion(machinestatus["barrel_temp_set"],[180,260])),
                        "BackPressureVsSuggestPressure":str(dp.check_backpressure(machinestatus["backpressure"],[4,5])),
                        "MaxInjectionPressureVsSettingPressure":str(dp.max_injection_pressure_compare_injection_pressure_setting(machinestatus["injection_pressure_list"],machinefeedback["Maximun_real_injection_pressure"])[0]),
                        "SettingPressureVsMachineLimitPressure":str(dp.settingpressure_vs_machinelimit(machinestatus["injection_pressure_list"],140)[0]),
                        "SettingSpeedVsMachineLimitSpeed":str(dp.settingspeed_vs_machinelimit(machinestatus["injection_speed"],200)[0]),
                        "MaxSpeedVsSpeedSetting":str(dp.compare_realinjection_ijspeedset(machinefeedback["maximun_real_injection_speed"],machinestatus["injection_speed"])[0]),
                        "HighSpeedRatio":str(dp.compare_max_ijspeed_postion(machinestatus["injection_speed"],machinestatus["injection_pos"])[0]),
                        "ShortShot":str(1)
                    }
            url = f"http://{self.hostip}:8000/smc/injectionmachinemes/troubleshooting/diagnosis"
            requestdata = {"machine_name":"FCS-150","evidences":evidences}
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
                    "自動轉保時間時間過短":[lambda: self.sloveshortfillingtimeset(machinestatus,deffectlevel)],
                    "射速過低":[lambda:  self.slovelowspeed(machinestatus,deffectlevel,200)],
                    "射壓過低":[lambda: self.slovelowpressure(machinestatus,deffectlevel,140)],
                    "計量不足":[lambda: self.slovelowdose(machinestatus,machinefeedback,deffectlevel)],
                    "背壓過低":[lambda:self.slovelowbackpressure()],
                    }
            modelresulttodb =""
            for reasonitem in DefectReason:
                modelresulttodb = modelresulttodb + reasonitem + ","
                for func in solution.get(reasonitem, []):
                    func()
            # Save for Train Data 
            modelresulttodb = modelresulttodb[:-1]
            url = f"http://{self.hostip}:8000/smc/injectionmachinemes/history/insertBayesianNetworkTrainData"
            storagerequestdata = {"machine_name":"FCS-150","modelresult":modelresulttodb}
            headers = {
                        'AccessToken': '8d6d4e85-b277-4102-8ffd-defcc7b7b9f9',
                        'Content-Type': 'application/json'
                    }
            response = requests.post(url,headers=headers, json=storagerequestdata)
                    
if __name__ == "__main__":
    processlineagent = fcstroubleshootagent("192.168.1.225")
    processlineagent.connect()