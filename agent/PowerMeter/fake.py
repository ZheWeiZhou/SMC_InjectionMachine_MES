import json
import redis
import time
redis_url= '140.135.106.49'
red= redis.Redis(host=redis_url,port=6379,db=0)
machine_name = 'cycu_test'
while True :
    time.sleep(2)
    print('machine up')
    machinestatus = {
        "machine":{'value':'work'}
    }
    red.set(f'{machine_name}_status',json.dumps(machinestatus))
    time.sleep(5)
    print('machine down')
    machinestatus = {
        "machine":{'value':'stay'}
    }
    red.set(f'{machine_name}_status',json.dumps(machinestatus))
    
    
