from pymodbus.client import ModbusTcpClient
import struct
import redis
import time
import json
from datetime import datetime
import math

class PVT_Collector:
    def __init__(self,redis_url,machineID,DAQIP):
        self.red= redis.Redis(host=redis_url,port=6379,db=0)
        self.machineID= machineID
        self.DAQIP = DAQIP
        self.DAQ= ''
        self.P1_list = []
        self.P2_list = []
        self.P3_list = []
        self.T1_list = []
        self.T2_list = []
        self.T3_list = []
        self.V1_list = []
        self.V2_list = []
        self.V3_list = []
        self.S1 = 47.98
        self.S2 = 47.53
        self.S3 = 47.79
        self.P_Reference1 = 0
        self.P_Reference2 = 100
        self.P_Reference3 = 200
        self.moldstatus = 0
        self.process_activate = 0
        self.moldclosecount = 0
        self.moldopencount = 0
        self.v_support_0 =[]
        self.v_support_50 =[]
        self.v_support_100 =[]
    def connect(self):
        self.DAQ = ModbusTcpClient(self.DAQIP, port=502)
        temprange = [50,75,100,125,150,175,200,225,250,275,300]
        for i in temprange:
            vsup0 = self.calspecificvolume(i,0)
            vsup50 = self.calspecificvolume(i,50)
            vsup100 = self.calspecificvolume(i,100)
            self.v_support_0.append(vsup0)
            self.v_support_50.append(vsup50)
            self.v_support_100.append(vsup100)


    def decode(self,high,low):
        raw_bytes = struct.pack('>HH', high, low)
        float_val = struct.unpack('>f', raw_bytes)[0]
        float_val = round(float_val, 2)
        return float_val
    def scale_adam_ai(self,raw_value):
        range_max = 10
        range_min = 0
        # 確保原始值在 16-bit 範圍內，避免異常數據
        if raw_value < 0: raw_value = 0
        if raw_value > 65535: raw_value = 65535
        # 線性換算公式: (原始值 / 最大階數) * 量程總長 + 最小值
        scaled_value = (raw_value / 65535.0) * (range_max - range_min) + range_min
        return round(scaled_value, 3)
    def getDAQDATA(self):
        AI = self.DAQ.read_holding_registers(address= 0, count =8).registers
        # for i in AI:
        #     print(i)
        moldclose = self.scale_adam_ai(AI[3])
        if moldclose > 8 :
            moldclose  = 1
        range = 10000  
        P1 = (self.scale_adam_ai(AI[0]) / self.S1) * range
        P1 = round(P1, 2)
        P2 = (self.scale_adam_ai(AI[1]) / self.S2) * range 
        P2 = round(P2, 2)
        P3 = (self.scale_adam_ai(AI[2]) / self.S3) * range
        P3 = round(P3, 2)
        T1 = self.scale_adam_ai(AI[4]) * 100
        T1 = round(T1, 2)
        T2 = self.scale_adam_ai(AI[5]) * 100
        T2 = round(T2, 2)
        T3 = self.scale_adam_ai(AI[6]) * 100
        T3 = round(T3, 2)
        data = {
            'P1':P1,
            'P2':P2,
            'P3':P3,
            'T1':T1,
            'T2':T2,
            'T3':T3,
            'moldclose':moldclose
        }
        return data
    def calspecificvolume(self,T,P):
        specificvolume = 0
        K = T + 273.15
        Pa = P * 10**6
        Tt = 417.15 + (2*10**(-8)*Pa)
        if K > Tt :
            V01= 0.836855 + (0.000444791 * (K-417.15))
            b3m = 1.84244 * 10**9
            B1 = b3m * math.exp(-0.003798 * (K-417.15) ) 
            specificvolume = V01 * (1-(0.0894* math.log(1+(Pa/B1)) ))
        else:
            b2s = 9.37625 * 10**(-5)
            V01 = 0.83695 + (b2s * (K-417.15))
            b3s = 2.45023 * 10**9
            B1 = b3s * math.exp(-0.00269261 * (K-417.15) ) 
            specificvolume = V01 * (1-(0.0894* math.log(1+(Pa/B1)) ))
        return specificvolume
    def collectdata(self):
        DAQRES = self.getDAQDATA()
        if DAQRES['moldclose'] == 1 :
            self.moldclosecount +=1
        if self.moldclosecount > 3:
            if self.process_activate == 0:
                self.moldopencount = 0
                self.process_activate = 1
            print(DAQRES)
            # chart X : T  Y:V 
            Pressure1 = DAQRES['P1']
            self.P1_list.append(Pressure1)
            Pressure2 = DAQRES['P2']
            self.P2_list.append(Pressure2)
            Pressure3 = DAQRES['P3']
            self.P3_list.append(Pressure3)
            Temp1 = DAQRES['T1'] 
            self.T1_list.append(Temp1)
            Temp2 = DAQRES['T2']
            self.T2_list.append(Temp2)
            Temp3 = DAQRES['T3']
            self.T3_list.append(Temp3)
            V1 = self.calspecificvolume(Temp1,Pressure1)
            self.V1_list.append(V1)
            V2 = self.calspecificvolume(Temp2,Pressure2)
            self.V2_list.append(V2)
            V3 = self.calspecificvolume(Temp3,Pressure3)
            self.V3_list.append(V3)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            pvtdata = {
                'P1':self.P1_list,
                'P2':self.P2_list,
                'P3':self.P3_list,
                'T1':self.T1_list,
                'T2':self.T2_list,
                'T3':self.T3_list,
                'V1':self.V1_list,
                'V2':self.V2_list,
                'V3':self.V3_list,
                'V_support_0':self.v_support_0,
                'V_support_50':self.v_support_50,
                'V_support_100':self.v_support_100,
                'updatetime':current_time
            }
        if DAQRES['moldclose'] == 0 :
            self.moldopencount +=1
        if self.moldopencount > 3:
            if self.process_activate == 1:
                max_val1 = max(self.T1_list)
                max_idx1 = self.T1_list.index(max_val1)
                max_val2 = max(self.T2_list)
                max_idx2 = self.T2_list.index(max_val2)
                max_val3 = max(self.T3_list)
                max_idx3 = self.T3_list.index(max_val3)
                pvtdata = {
                'P1':self.P1_list[max_idx1:],
                'P2':self.P2_list[max_idx2:],
                'P3':self.P3_list[max_idx3:],
                'T1':self.T1_list[max_idx1:],
                'T2':self.T2_list[max_idx2:],
                'T3':self.T3_list[max_idx3:],
                'V1':self.V1_list[max_idx1:],
                'V2':self.V2_list[max_idx2:],
                'V3':self.V3_list[max_idx3:],
                'V_support_0':self.v_support_0,
                'V_support_50':self.v_support_50,
                'V_support_100':self.v_support_100,
                'updatetime':current_time
            }
                self.red.set(f'{self.machineID}_pvt',json.dumps(pvtdata))
                self.moldclosecount =0
                self.process_activate = 0
                self.P1_list = []
                self.P2_list = []
                self.P3_list = []
                self.T1_list = []
                self.T2_list = []
                self.T3_list = []
                self.V1_list = []
                self.V2_list = []
                self.V3_list = []

if __name__ == "__main__":
    machineID= 'FCS-150'
    redis_url= '140.135.106.49'
    daqip ='192.168.200.20'
    worker = PVT_Collector(redis_url,machineID,daqip)
    worker.connect()
    while True :
       worker.collectdata()
       time.sleep(0.1)




        
        






    



