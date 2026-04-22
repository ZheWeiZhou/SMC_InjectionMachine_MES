from datetime import datetime
import json
import redis
import random
class PowerMeterWorker:
    def __init__(self,redis_url,machineID):
        self.red= redis.Redis(host=redis_url,port=6379,db=0)
        self.machineID= machineID
        self.current_curve_a =[]
        self.current_curve_b =[]
        self.current_curve_c =[]
        self.process_activate = False
    def collectcurrent(self):
        base_current= 5.0
        current_a = round(random.uniform(base_current * 0.95, base_current * 1.05), 2)
        current_b = round(random.uniform(base_current * 0.95, base_current * 1.05), 2)
        current_c = round(random.uniform(base_current * 0.95, base_current * 1.05), 2)

        current={
            "current_a":current_a,
            "current_b":current_b,
            "current_c":current_c,
        }
        currenttime= datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'PowerMeter_{self.machineID}_current_updatetime',currenttime)
        self.red.set(f'PowerMeter_{self.machineID}_current',json.dumps(current))
        machinestatus   = self.red.get(f'{self.machineID}_status')
        machinestatus   = json.loads(machinestatus)
        if machinestatus['machine']['value'] != 'stay':
            if self.process_activate == False:
                self.current_curve_a= []
                self.current_curve_b= [] 
                self.current_curve_c =[]
            self.process_activate = True
            self.current_curve_a.append(current_a)
            self.current_curve_b.append(current_b)
            self.current_curve_c.append(current_c)
        else :
            if self.process_activate == True:
                print("update curve")
                current_curve ={
                    "current_a":self.current_curve_a,
                    "current_b":self.current_curve_b,
                    "current_c":self.current_curve_c,
                    "updated_time":currenttime
                }
                self.red.set(f'PowerMeter_{self.machineID}_currentcurve_updatetime',currenttime)
                self.red.set(f'PowerMeter_{self.machineID}_currentcurve',json.dumps(current_curve))
                self.process_activate = False



if __name__ == "__main__":
    machineID= 'cycu_test'
    redis_url= '140.135.106.49'
    worker= PowerMeterWorker(redis_url,machineID)
    while True:
        worker.collectcurrent()
        # try:
        #     worker.collectcurrent()
        # except:
        #     pass