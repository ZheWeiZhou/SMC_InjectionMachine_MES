from pymodbus.client import ModbusSerialClient,ModbusTcpClient
import struct
import redis
import time
import json
from datetime import datetime
from pprint import pprint
import numpy as np


import matplotlib.pyplot as plt

def plot_line_chart(data, vlines=None, title="Data Plot", xlabel="Index", ylabel="Value"):
    """
    繪製折線圖並支援垂直線功能
    :param data: 數據列表
    :param vlines: 垂直線的位置列表 (例如: [10, 50, 100])
    :param title: 圖表標題
    :param xlabel: X軸標籤
    :param ylabel: Y軸標籤
    """
    plt.figure(figsize=(12, 6))
    
    # 繪製主折線
    plt.plot(data, marker='', linestyle='-', linewidth=1.5, label='Data')
    
    # 加入垂直線
    if vlines:
        for x in vlines:
            plt.axvline(x=x, color='r', linestyle='--', alpha=0.7, label=f'Event at {x}')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()



class ActionDetecter:
    def __init__(self,DAQIP):
        self.DAQIP = DAQIP
        self.Detecter = ''
    def connect(self):
        self.Detecter = ModbusTcpClient(self.DAQIP, port=502)
    def get_machine_status(self):
        # rawbyte = self.Detecter.read_input_registers(address=1024, count=3)
        # print(rawbyte)
        status = {
            "Injection":0,
            "Packing":0,
            "MoldOpen":0
        }
        result = self.Detecter.read_discrete_inputs(address=0, count=3)
        # print(result.bits)
        status["MoldOpen"] = result.bits[0]
        status["Injection"] = result.bits[1]
        status["Packing"] = result.bits[2]
        x0 = result.bits[0]
        x1 = result.bits[1]
        x2 = result.bits[2]
        # print(f"x0: {x0} x1: {x1} x2: {x2}")
        # print(f"在 Holding Register {21} 讀到非零值: {bin(result.registers[0])}")
        # for addr in range(0, 100): # 掃描前 100 個暫存器
        #     result = self.Detecter.read_holding_registers(address=addr, count=1)
        #     if not result.isError():
        #         # 如果讀到了數值，印出來看看 (這數值可能包含多個 X 點的狀態)
        #         if result.registers[0] != 0:
        #             print(f"在 Holding Register {addr} 讀到非零值: {bin(result.registers[0])}")
        return status


class DeltaPowerMeterRTUAgent:
    def __init__(self,redis_url,machineID,comport,baudrate,actiondetecter):
        self.red= None
        if redis_url is not None:
            self.red= redis.Redis(host=redis_url,port=6379,db=0)
        self.machineID = machineID
        self.current_curve_a =[]
        self.current_curve_b =[]
        self.current_curve_c =[]
        self.voltage_curve_ab =[]
        self.voltage_curve_bc =[]
        self.voltage_curve_ca =[]
        self.power_curve =[]
        self.process_activate = False
        self.powermeter = ''
        self.comport = comport
        self.baudrate = baudrate
        self.actiondetecter = actiondetecter
        self.moldcloseactivate = 0
        self.injection_start_index = -1
        self.injection_end_index = -1
        self.packing_start_index = -1
        self.packing_end_index = -1
        self.collectstarttime = -1
        self.collectendtime = -1
        
    def conncet(self):
        powermeter = ModbusSerialClient(
            port=self.comport,    # Windows 環境請改成 'COM5' 等形式
            baudrate=self.baudrate,        # 波特率
            bytesize=8,           # 資料位元
            parity='N',           # 校驗位: 'N' (None), 'E' (Even), 'O' (Odd)
            stopbits=1,           # 停止位
            timeout=1             # 超時時間（秒）
        )
        self.powermeter = powermeter
    def decode(self,high,low):
        raw_bytes = struct.pack('>HH', high, low)
        float_val = struct.unpack('>f', raw_bytes)[0]
        float_val = round(float_val, 2)
        return float_val
    
    def calculate_3p_energy_curve_full(self, va_list, vb_list, vc_list, ia_list, ib_list, ic_list, total_time, power_factor=0.9):
        """
        計算完整三相電（三相電壓與三相電流曲線）的耗電量
        並回傳「每個採樣區間」的單純耗電量 (kJ) 曲線
        """
        # 轉換為 numpy 陣列
        va_arr = np.array(va_list)
        vb_arr = np.array(vb_list)
        vc_arr = np.array(vc_list)
        ia_arr = np.array(ia_list)
        ib_arr = np.array(ib_list)
        ic_arr = np.array(ic_list)
        
        n = len(va_arr)
        if n == 0:
            return 0.0, np.array([])
            
        dt = total_time / n
        
        # 1. 計算每個採樣點的時間平均線電壓與平均線電流
        v_avg_arr = (va_arr + vb_arr + vc_arr) / 3.0
        i_avg_arr = (ia_arr + ib_arr + ic_arr) / 3.0
        
        # 2. 計算每個點的瞬時總功率 P = sqrt(3) * V_avg * I_avg * PF (單位: Watts)
        instant_powers = np.sqrt(3) * v_avg_arr * i_avg_arr * power_factor
        
        # 3. 計算每個時間區間的實際消耗能量 dE = P * dt / 1000 (單位: kJ)
        interval_energy_kj = (instant_powers * dt) / 1000
        
        # 4. 計算這段時間的總累積耗電量
        total_energy_kj = np.sum(interval_energy_kj)
        
        return total_energy_kj, interval_energy_kj

    def calPower(self,powercurve,timedelta):
        energy_ws = 0
        for i in range(len(powercurve) - 1):
            p1 = powercurve[i]
            p2 = powercurve[i + 1]
            # 梯形積分
            energy_ws += ((p1 + p2) / 2) * timedelta
        energy_kj = energy_ws / 1000
        return energy_kj
    def modifyinjectionstartindex(self,curve):
        arr = np.array(curve)
        # 計算相鄰點的差值絕對值
        gradient_abs = np.abs(np.diff(arr))
        max_grad_index = np.argmax(gradient_abs)
        return max_grad_index
    def collectdata(self):
        try:
            rawbyte = self.powermeter.read_holding_registers(address=264, count=30).registers
            voltage_ab = self.decode(rawbyte[0],rawbyte[1])
            voltage_bc = self.decode(rawbyte[2],rawbyte[3])
            voltage_ca = self.decode(rawbyte[4],rawbyte[5])
            current_a = self.decode(rawbyte[24],rawbyte[25])
            current_b = self.decode(rawbyte[26],rawbyte[27])
            current_c = self.decode(rawbyte[28],rawbyte[29])
            powerrawbyte = self.powermeter.read_holding_registers(address=324, count=2).registers
            power = self.decode(powerrawbyte[0],powerrawbyte[1])
            powermeterinfo = {
                "current_a":current_a,
                "current_b":current_b,
                "current_c":current_c,
                "voltage_ab":voltage_ab,
                "voltage_bc":voltage_bc,
                "voltage_ca":voltage_ca,
                "power":power,
            }
            # pprint(powermeterinfo)
            # print('=' * 30)
            return powermeterinfo
        except Exception as e:
            print(e)
    def workflow(self):
        powermeterinfo = self.collectdata()
        if self.red is not None:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.red.set(f'PowerMeter_{self.machineID}_realtime_current_updatetime',current_time)
            self.red.set(f'PowerMeter_{self.machineID}_realtime_current_',json.dumps(powermeterinfo))
        machinestatus = self.actiondetecter.get_machine_status()
        if machinestatus["MoldOpen"] == False:
            if self.moldcloseactivate == 0:
                print('MoldClose')
                self.collectstarttime = time.perf_counter()

            self.moldcloseactivate = 1
            self.current_curve_a.append(powermeterinfo["current_a"])
            self.current_curve_b.append(powermeterinfo["current_b"])
            self.current_curve_c.append(powermeterinfo["current_c"])
            self.voltage_curve_ab.append(powermeterinfo["voltage_ab"])
            self.voltage_curve_bc.append(powermeterinfo["voltage_bc"])
            self.voltage_curve_ca.append(powermeterinfo["voltage_ca"])
            self.power_curve.append(powermeterinfo["power"])
            if machinestatus["Injection"] == True:
                if self.injection_start_index == -1:
                    print('Injection Start')
                    self.injection_start_index = len(self.current_curve_a)  +18
            if machinestatus["Injection"] == False:
                if self.injection_start_index != -1 and self.injection_end_index == -1:
                    self.injection_end_index = len(self.current_curve_a)  +18
            if machinestatus["Packing"] == True:
                if self.packing_start_index == -1:
                    print('Packing Start')
                    self.packing_start_index = len(self.current_curve_a) +18
            if machinestatus["Packing"] == False:
                if self.packing_start_index != -1 and self.packing_end_index == -1:
                    self.packing_end_index = len(self.current_curve_a)  +18
        else:
            if self.moldcloseactivate == 1:
                self.collectendtime = time.perf_counter()
                totaltime = self.collectendtime - self.collectstarttime
                injectionpowersearchreange = self.power_curve[self.injection_start_index-20:self.injection_start_index]
                injectionsigindex = self.modifyinjectionstartindex(injectionpowersearchreange)
                self.injection_start_index = self.injection_start_index - len(injectionpowersearchreange) + injectionsigindex
                self.packing_start_index = self.packing_start_index - len(injectionpowersearchreange) + injectionsigindex
                self.packing_end_index = self.packing_end_index - len(injectionpowersearchreange) + injectionsigindex
                injection_power_curve = self.power_curve[self.injection_start_index:self.packing_start_index]
                packing_power_curve = self.power_curve[self.packing_start_index:self.packing_end_index]
                open_mold_power_curve = self.power_curve[self.packing_end_index:]
                timedelta = totaltime/len(self.power_curve)
                injectiontotalpower = self.calPower(injection_power_curve,timedelta)
                packingtotalpower = self.calPower(packing_power_curve,timedelta)
                openmoldtotalpower = self.calPower(open_mold_power_curve,timedelta)
                print(f"injectiontotalpower: {injectiontotalpower} Kj, packingtotalpower: {packingtotalpower} Kj, openmoldtotalpower: {openmoldtotalpower} Kj")
                # vlines_position = [self.injection_start_index, self.packing_start_index, self.packing_end_index]
                # plot_line_chart(self.power_curve, vlines=vlines_position, title="機台功耗監控")
                powersummary = {
                    "injectiontotalpower":injectiontotalpower,
                    "packingtotalpower":packingtotalpower,
                    "openmoldtotalpower":openmoldtotalpower,
                    "powercurve":self.power_curve,
                }
                self.red.set(f'PowerMeter_{self.machineID}_powersummary',json.dumps(powersummary))
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                self.red.set(f'PowerMeter_{self.machineID}__powersummary_updatetime',current_time)
                """
                這邊把每個動作的能耗都算完然後上拋
                """
                # totalenergy , energycurve = self.calculate_3p_energy_curve_full(self.voltage_curve_ab,self.voltage_curve_bc,self.voltage_curve,totaltime)
                self.moldcloseactivate = 0
                self.injection_start_index = -1
                self.injection_end_index = -1
                self.packing_start_index = -1
                self.packing_end_index = -1
                self.current_curve_a = []
                self.current_curve_b = []
                self.current_curve_c = []
                self.voltage_curve_ab = []
                self.voltage_curve_bc = []
                self.voltage_curve_ca = []
                self.collectstarttime = -1
                self.collectendtime = -1
                self.power_curve = []

if __name__ == "__main__":
    actiondetecter = ActionDetecter("192.168.1.18")
    actiondetecter.connect()

    redis_url= "140.135.106.49"
    machineID = "Tachung"
    agent = DeltaPowerMeterRTUAgent(redis_url,machineID,'COM5',115200,actiondetecter)
    agent.conncet()
    while True:
        time.sleep(0.001)
        agent.workflow()
        
