from datetime import datetime
import json
import redis
import random
class PowerMeterWorker:
    def __init__(self,redis_url,machineID):
        self.red= redis.Redis(host=redis_url,port=6379,db=0)
        self.machineID= machineID
    def collectcurrent(self):
        base_current= 15.0
        current={
            "current_a":round(random.uniform(base_current * 0.95, base_current * 1.05), 2),
            "current_b":round(random.uniform(base_current * 0.95, base_current * 1.05), 2),
            "current_c":round(random.uniform(base_current * 0.95, base_current * 1.05), 2),
        }
        currenttime= datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'PowerMeter_{self.machineID}_updatetime',currenttime)
        self.red.set(f'PowerMeter_{self.machineID}_current',json.dumps(current))

if __name__ == "__main__":
    machineID= 'Engel120'
    redis_url= '140.135.106.49'
    worker= PowerMeterWorker(redis_url,machineID)
    while True:
        try:
            worker.collectcurrent()
        except:
            pass