from datetime import datetime
import json
import redis

with open('config.json', 'r', encoding='utf-8') as f:
    envparameter = json.load(f)
class PowerMeterCollecter:
    def __init__(self):
        self.red= redis.Redis(host=envparameter["red_url"],port=6379,db=0)
    def getcurrent(self,machineID):
        current_response={
            "current_a":-1,
            "current_b":-1,
            "current_c":-1,
            "online": False
            }
        powermeterupdatetime= self.red.get(f"PowerMeter_{machineID}_current_updatetime")
        if powermeterupdatetime is None:
            return current_response
        powermeterupdatetime = powermeterupdatetime.decode('utf-8')
        datetime_obj = datetime.strptime(powermeterupdatetime, "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        time_difference = current_time - datetime_obj
        seconds_diff = time_difference.total_seconds()
        if seconds_diff >5:
            return current_response
        raw_current= self.red.get(f"PowerMeter_{machineID}_current")
        if raw_current:
            current_response= json.loads(raw_current)
            current_response["online"]= True
        return current_response
    def getcurrentcurve(self,machineID):
        current_curve={
            "current_a":[-1],
            "current_b":[-1],
            "current_c":[-1],
            "updatetime":-1
            }
        powermeterupdatetime= self.red.get(f"PowerMeter_{machineID}_currentcurve_updatetime")
        raw_currentcurve= self.red.get(f"PowerMeter_{machineID}_currentcurve")
        if powermeterupdatetime and raw_currentcurve:
            current_curve =json.loads(raw_currentcurve)
            current_curve["updatetime"] =powermeterupdatetime.decode('utf-8')
            return current_curve
        return current_curve

        

        


