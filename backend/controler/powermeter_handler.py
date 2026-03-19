from datetime import datetime
import json
import redis

class PowerMeterCollecter:
    def __init__(self):
        self.red= redis.Redis(host='Redis',port=6379,db=0)
    def getcurrent(self,machineID):
        current_response={
            "current_a":-1,
            "current_b":-1,
            "current_c":-1,
            }
        powermeterupdatetime= self.red.get(f"PowerMeter_{machineID}_updatetime").decode('utf-8')
        if powermeterupdatetime is None:
            return current_response
        datetime_obj = datetime.strptime(powermeterupdatetime, "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        time_difference = current_time - datetime_obj
        seconds_diff = time_difference.total_seconds()
        if seconds_diff >5:
            return current_response
        raw_current= self.red.get(f"PowerMeter_{machineID}_current")
        if raw_current:
            current_response= json.loads(raw_current)
        return current_response
        


