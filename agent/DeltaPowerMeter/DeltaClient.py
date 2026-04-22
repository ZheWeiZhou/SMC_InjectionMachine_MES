from pymodbus.client import ModbusTcpClient
import struct
import redis
import time
import json
from datetime import datetime
from opcua import Client
from opcua import ua
class DeltaPowerMeterAgent:
    def __init__(self,redis_url,machineID,machineaddress,powermeterIP):
        self.red= redis.Redis(host=redis_url,port=6379,db=0)
        self.machineID= machineID
        self.current_curve_a =[]
        self.current_curve_b =[]
        self.current_curve_c =[]
        self.voltage_curve_ab =[]
        self.voltage_curve_bc =[]
        self.voltage_curve_ca =[]
        self.process_activate = False
        self.powermeterIP = powermeterIP
        self.powermeter = ''
        self.starttimestemp = ''
        self.machineaddress = machineaddress
        self.worker = ''
        self.lastscrewpos = ''
        self.plastizestart = False
        self.finishplastize = False
    def conncet(self):
        self.powermeter = ModbusTcpClient(self.powermeterIP, port=502)
        url="opc.tcp://"+self.machineaddress
        self.worker=Client(url)
        self.worker.connect()
    def decode(self,high,low):
        raw_bytes = struct.pack('>HH', high, low)
        float_val = struct.unpack('>f', raw_bytes)[0]
        float_val = round(float_val, 2)
        return float_val
    def collect(self):
        processstatus  = self.worker.get_node("ns=4;s=APPL.Injection1.do_Inject").get_value()
        plastizesignal = self.worker.get_node("ns=4;s=APPL.Injection1.do_Plasticize").get_value()
        rawbyte = self.powermeter.read_holding_registers(address= 265, count =30).registers
        voltage_ab = self.decode(rawbyte[0],rawbyte[1])
        voltage_bc = self.decode(rawbyte[2],rawbyte[3])
        voltage_ca = self.decode(rawbyte[4],rawbyte[5])
        current_a = self.decode(rawbyte[24],rawbyte[25])
        current_b = self.decode(rawbyte[26],rawbyte[27])
        current_c = self.decode(rawbyte[28],rawbyte[29])
        if processstatus is True:

            if self.process_activate == False:
                print('Process start')
                self.starttimestemp = time.perf_counter()
                self.current_curve_a= []
                self.current_curve_b= [] 
                self.current_curve_c =[]
                self.voltage_curve_ab =[]
                self.voltage_curve_bc =[]
                self.voltage_curve_ca =[]
            self.current_curve_a.append(current_a)
            self.current_curve_b.append(current_b)
            self.current_curve_c.append(current_c)
            self.voltage_curve_ab.append(voltage_ab)
            self.voltage_curve_bc.append(voltage_bc)
            self.voltage_curve_ca.append(voltage_ca)
            self.process_activate = True
        elif plastizesignal is True :
            if self.plastizestart is False:
                print('DETECT Plastize')
                self.plastizestart =True
            self.current_curve_a.append(current_a)
            self.current_curve_b.append(current_b)
            self.current_curve_c.append(current_c)
            self.voltage_curve_ab.append(voltage_ab)
            self.voltage_curve_bc.append(voltage_bc)
            self.voltage_curve_ca.append(voltage_ca)       
        else:
            if self.process_activate == True and self.plastizestart is True:
                print("FINISH PLASTIZE")
                endtime = time.perf_counter()
                totaltime = endtime - self.starttimestemp
                print(f'total process {totaltime}')
                print("update curve")
                machinepowerinfo ={}
                curve = {
                    "current_curve_a":{
                        "value":self.current_curve_a,
                        "name":"Current A",
                        "Unit": "A"
                    },
                    "current_curve_b":{
                        "value":self.current_curve_b,
                        "name":"Current B",
                        "Unit": "A"
                    },
                    "current_curve_c":{
                        "value":self.current_curve_c,
                        "name":"Current C",
                        "Unit": "A"
                    },
                    "voltage_curve_ab":{
                        "value":self.voltage_curve_ab,
                        "name":"Voltage AB",
                        "Unit": "V"
                    },   
                    "voltage_curve_bc":{
                        "value":self.voltage_curve_bc,
                        "name":"Voltage BC",
                        "Unit": "V"
                    }, 
                    "voltage_curve_ca":{
                        "value":self.voltage_curve_ca,
                        "name":"Voltage CA",
                        "Unit": "V"
                    },                                 
                }
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                machinepowerinfo["updatetime"] = current_time
                machinepowerinfo["abstract"] = {}
                machinepowerinfo["curve"] = curve
                self.red.set(f'{self.machineID}_energy',json.dumps(machinepowerinfo))
                self.process_activate = False
                self.plastizestart = False
                self.finishplastize = False

if __name__ == "__main__":
    machineID= 'FCS-150'
    redis_url= '140.135.106.49'
    powermeterip ='192.168.3.5'
    machineaddress = '192.168.1.12:4842'
    worker= DeltaPowerMeterAgent(redis_url,machineID,machineaddress,powermeterip)
    worker.conncet()
    while True:
        time.sleep(0.01)
        worker.collect()
        # try:
        #     worker.collect()
        # except:
            
        #     pass
    # while True:
    #     worker.collectcurrent()


# from modbus_tk import modbus_tcp

# # 建立 TCP Master
# master = modbus_tcp.TcpMaster(host=IP_ADDRESS, port=PORT)

# master.set_timeout(5.0)
# for fc in [3, 4]:
#     print("Function:", fc)
#     for addr in range(250, 265):
#         try:
#             result = master.execute(1, fc, addr, 1)
#             print("OK", fc, addr, result)
#         except:
#             pass



# client = ModbusTcpClient(IP_ADDRESS, port=PORT)
# def decode(high,low):
#     raw_bytes = struct.pack('>HH', high, low)
#     float_val = struct.unpack('>f', raw_bytes)[0]
#     float_val = round(float_val, 1)
#     return float_val
# step = 1
# if client.connect():
#     # 3. 讀取 D 點 (Holding Register)
#     # address: D點位址 (例如 D0 就是 0)
#     # count: 要讀取的數量
#     # slave: 從站 ID (通常是 1)
#     address = 289
#     count = 6
#     start_time = time.perf_counter()
#     while True:
#         time.sleep(0.05)

#         result = client.read_holding_registers(address= address, count =count)
#         reg =[]
#         volreg = []

#         if not result.isError():
#             # 取得讀取到的數值清單
#             d_values = result.registers
#             for i in d_values:
#                 reg.append(i)
#             current_a = decode(reg[0],reg[1])
#             current_b = decode(reg[2],reg[3])
#             current_c = decode(reg[4],reg[5])
            
#             # step +=1
#         voltage = client.read_holding_registers(address= 265, count =6)
#         if not voltage.isError():
#             # 取得讀取到的數值清單
#             vol_values = voltage.registers
#             print(voltage.registers)
#             # for v in vol_values:
#             #     volreg.append(v)
#             # voltage_ab = decode(volreg[0],volreg[1])
#             # voltage_bc = decode(volreg[2],volreg[3])
#             # voltage_ca = decode(volreg[4],volreg[5])
#         #     break
#             print(f"電流 : A: {current_a} B: {current_b} C: {current_c} ")
#             print(f"電壓 AB {voltage_ab} BC {voltage_bc} CA {voltage_ca}")

#         else:
#             pass

#     # 4. 關閉連線
#     client.close()
# else:
#     print("無法連線至 Modbus 設備")