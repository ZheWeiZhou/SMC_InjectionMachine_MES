from datetime import datetime
import json
import redis

with open('config.json', 'r', encoding='utf-8') as f:
    envparameter = json.load(f)
class MachineEndSignalHandler:
    def __init__(self):
        self.red= redis.Redis(host=envparameter["red_url"],port=6379,db=0)
    def getfeedbackupdatetime(self,machineID):
        machinefeedback = self.red.get(f'{machineID}_feedback')
        machinefeedback = json.loads(machinefeedback)
        updatetime = machinefeedback["updatetime"]
        return updatetime

        

        


