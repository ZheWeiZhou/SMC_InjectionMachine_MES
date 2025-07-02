import serial
from modbus_tk import defines
import modbus_tk.modbus_rtu as modbus_rtu
import time
import cv2
import uuid
import base64
import numpy as np
import tensorflow as tf
import redis
from mettler_toledo_device import MettlerToledoDevice
import json
from datetime import datetime, timezone
class Process_line_agent:
    def __init__(self,
        serial_port = "COM4",
        baudrate = 115200,#鮑率
        bytesize = 8,
        parity = "N", #無校驗
        stopbits = 1 , #停止位元
        aoimodel =''
    ):
        self.serial_port=serial_port
        self.baudrate=baudrate
        self.bytesize=bytesize
        self.parity=parity
        self.stopbits=stopbits
        self.master=''
        self.cap=''
        self.aoimodel=aoimodel
        self.weightmeter=MettlerToledoDevice(port='COM8')
        self.red=redis.Redis(host='192.168.1.225',port=6379,db=0)
    def connect(self):
        try:
            self.master=modbus_rtu.RtuMaster(
                serial.Serial(port=self.serial_port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits)
            )
            self.master.set_timeout(10.0)
            print("[INFO] Process Line Agent connect success")
        except:
            RuntimeError("[ERROR]: Connect failed...")
    def opencamera(self):
        self.cap=cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2456)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,2054)
    def modelupdate(self,filename):
        self.aoimodel=tf.keras.models.load_model(filename)
    def capturefig(self):
        self.cap=cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2456)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,2054)
        ret, frame = self.cap.read()
        if ret:
            resized_frame = cv2.resize(frame, (1200, 800))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(gray_frame,50,255, cv2.THRESH_BINARY)
            for_ratio_draw=thresh.copy()
            zeropixel=np.count_nonzero(for_ratio_draw==0)
            imgarea=resized_frame.shape[0]*resized_frame.shape[1]
            ratio=zeropixel/imgarea
            shortshotratio=ratio/0.576178
            gray_frame_3_channels = np.stack((gray_frame,) * 3, axis=-1)
            imageinput=cv2.resize(gray_frame_3_channels, dsize=(80, 80))

            imageinput=np.array([imageinput])
            ans=self.aoimodel.predict(imageinput)
            prediction='normal'
            print(f'[DEBUG] aoi predict {ans[0]}')
            if ans[0] >0.5:
                prediction='shortshot'
            figname=uuid.uuid4()
            #picture encode to base64
            success, encoded_image = cv2.imencode('.jpg', resized_frame)
            encoded_image_str=''
            if success:
                encoded_image_str = base64.b64encode(encoded_image.tobytes()).decode('utf-8')
            cv2.imwrite(f"{figname}.jpg", resized_frame)
        self.cap.release()
        return figname,encoded_image_str,prediction,shortshotratio
    def readdouble_register(self,slave_address,register_address):
        try:
            self.master.open()
            data = self.master.execute(slave=slave_address, function_code=defines.READ_HOLDING_REGISTERS,  starting_address=register_address, quantity_of_x=2,)# register_address:讀取起始位址(10進制的整數) ;1:讀取長度
            combined_value = (data[0] << 16) | data[1]
            signed_integer = combined_value if combined_value < 0x80000000 else combined_value - 0x100000000
            decimal_value = int(signed_integer)
            return decimal_value
        except:
            RuntimeError("[DUMMY ERROR]: Read register failed...")
        finally:
            self.master.close()
    def readsingle_register(self,slave_address,register_address):
        try:
            self.master.open()
            data = self.master.execute(slave=slave_address, function_code=defines.READ_HOLDING_REGISTERS,  starting_address=register_address, quantity_of_x=1)# register_address:讀取起始位址(10進制的整數) ;1:讀取長度

            return data
        except:
            RuntimeError("[DUMMY ERROR]: Read register failed...")
        finally:
            self.master.close()
    def write_singleregister(self,slave_address,register_address,value):
        try:
            self.master.open()
            self.master.execute(slave=slave_address, function_code=defines.WRITE_SINGLE_REGISTER, starting_address=register_address, output_value=value)
        except:
            RuntimeError("[DUMMY ERROR]: Write register failed...")
        finally:
            self.master.close()
    def write_batchregister(self,slave_address,register_address,value):
        try:
            self.master.open()
            decimal_value_to_write =value
            binary_value = bin(decimal_value_to_write)[2:].zfill(32)
            high_bits = int(binary_value[:16], 2)
            low_bits = int(binary_value[16:], 2)
            self.master.execute(slave=slave_address, function_code=defines.WRITE_SINGLE_REGISTER, starting_address=register_address, output_value=high_bits)
            self.master.execute(slave=slave_address, function_code=defines.WRITE_SINGLE_REGISTER, starting_address=register_address+1, output_value=low_bits)
        except:
            RuntimeError("[DUMMY ERROR]: Write register failed...")
        finally:
            self.master.close()
    
def processlinereset():
    print("[Message] Start to reset process line ...")
    agent.write_batchregister(3,118,2) #切換成地0個job
    agent.write_singleregister(3,125,32)#先把指令reset成stop
    agent.write_singleregister(3,125,16)#命令job作動
    agent.write_batchregister(4,118,1) #切換成地0個job
    agent.write_singleregister(4,125,32)#先把指令reset成stop
    agent.write_singleregister(4,125,16)#命令job作動
    jobfinish=0
    jobcount = 0
    while jobfinish==0:
        time.sleep(1)
        jobcount +=1
        result=agent.readsingle_register(3,127)
        if int(result[0])==8 or jobcount >50: #觀察job是否完成
            jobfinish=1
def weightmeterreset():
    print("Start reset weight meter")
    weightreset=0
    while weightreset==0:
        time.sleep(1)
        agent.weightmeter.zero_stable()
        weight=agent.weightmeter.get_weight()[0]
        print(abs(weight))
        if abs(weight) <0.1:
            weightreset=1
            print('Weight meter success reset')    

def processlinemove():
    print("[MESSAGE] TASK START")
    #把產品移到鏡頭下
    agent.write_batchregister(3,118,0) #切換成地0個job
    agent.write_singleregister(3,125,32)#先把指令reset成stop
    agent.write_singleregister(3,125,8)#命令job作動
    jobfinish=0
    while jobfinish==0:
        time.sleep(0.2)
        result=agent.readsingle_register(3,127)
        
        if int(result[0])==8: #觀察job是否完成
            jobfinish=1
    # #拍照
    figname,encoded_image_str,prediction,shortshotratio = agent.capturefig()

    #調整分類隔板================
    if prediction == "shortshot":
        classfication('b')
    if prediction == "normal":
        classfication('c')
    #=============================
    #產品移到要被分類的地方
    agent.write_batchregister(3,118,1)
    agent.write_singleregister(3,125,32)
    agent.write_singleregister(3,125,8)
    jobfinish=0
    while jobfinish==0:
        result=agent.readsingle_register(3,127) 
        if int(result[0])==8: #觀察job是否完成
            jobfinish=1
    # time.sleep(3)

    #撥下去
    agent.write_batchregister(4,118,0)
    agent.write_singleregister(4,125,32)
    agent.write_singleregister(4,125,8)
    jobfinish=0
    while jobfinish==0:
        result=agent.readsingle_register(4,127)
        
        if int(result[0])==8: #觀察job是否完成
            jobfinish=1
    # #===================================
    # #產線那隻復歸
    agent.write_batchregister(3,118,2)
    agent.write_singleregister(3,125,32)
    agent.write_singleregister(3,125,8)
    jobfinish=0
    while jobfinish==0:
        result=agent.readsingle_register(3,127)
        if int(result[0])==8: #觀察job是否完成
            jobfinish=1
    #撥桿復歸
    agent.write_batchregister(4,118,1)
    agent.write_singleregister(4,125,32)
    agent.write_singleregister(4,125,8)
    # agent.write_batchregister(3,118,4)
    # agent.write_singleregister(3,125,32)
    # agent.write_singleregister(3,125,8)
    agent.write_batchregister(3,118,2) #切換成地0個job
    agent.write_singleregister(3,125,32)#先把指令reset成stop
    agent.write_singleregister(3,125,16)#命令job作動
    time.sleep(3)
    return encoded_image_str, prediction, 

def classfication(type): #分類
    if type=='a':
        print(0)
        agent.write_batchregister(2,118,0)
        agent.write_singleregister(2,125,32)
        agent.write_singleregister(2,125,8)
        agent.write_batchregister(1,118,0)
        agent.write_singleregister(1,125,32)
        agent.write_singleregister(1,125,8)
        print(1)
        b=0
        while b==0:
            result1=agent.readsingle_register(2,127)
            result2=agent.readsingle_register(1,127)
            print(f'2 {result1} {result2}')
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
    if type=='b':
        agent.write_batchregister(2,118,0)
        agent.write_singleregister(2,125,32)
        agent.write_singleregister(2,125,8)
        agent.write_batchregister(1,118,1)
        agent.write_singleregister(1,125,32)
        agent.write_singleregister(1,125,8)
        b=0
        while b==0:
            result1=agent.readsingle_register(2,127)
            result2=agent.readsingle_register(1,127)
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
    if type=='c':
        agent.write_batchregister(2,118,1)
        agent.write_singleregister(2,125,32)
        agent.write_singleregister(2,125,8)
        agent.write_batchregister(1,118,1)
        agent.write_singleregister(1,125,32)
        agent.write_singleregister(1,125,8)
        b=0
        while b==0:
            result1=agent.readsingle_register(2,127)
            result2=agent.readsingle_register(1,127)
            if int(result1[0])==8 and int(result2[0])==8:
                b=1
weightconfirm = 0
def workflow():
    global weightconfirm
    while True:
        time.sleep(1)
        # reset_command = agent.red.get('Process_Line_reset_command').decode('utf-8')
        # if reset_command =='on':
        #     print('[Message] Start to reset process line ...')
        #     processlinereset()
        #     weightmeterreset()
        #     agent.red.set('Process_Line_reset_command','off')
        try:
            weight=agent.weightmeter.get_weight()[0]
            if weight >5:
                print("[Message] Detect weight")
                weightconfirm += 1
                if weightconfirm >5:
                    agent.red.set('FCS-150_Process_Line_status','processing')
                    print("[Message] Detect there is product on the platfrom")
                    product_weight = agent.weightmeter.get_weight()[0]
                    encoded_image_str, productquality = processlinemove()
                    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                    shortshotratio = 0 
                    if productquality == "shortshot":
                        shortshotratio = 1 - weight/19
                    message = {'created_time':utc_now,'product_weight':product_weight, 'image_str':encoded_image_str,'quality':productquality, 'shortshotratio':shortshotratio}
                    message_dump = json.dumps(message)
                    agent.red.set('FCS-150_Process_Line_message',message_dump)
                    print(f"[Message] Finish Process Product quality: {productquality} Product weight :{weight} Shortshotratio : {shortshotratio}")
                    weightmeterreset()
                    time.sleep(1)
                    agent.red.set('FCS-150_Process_Line_status','standby')
        
            else:
                agent.red.set('FCS-150_Process_Line_status','standby')
                # print("[Message] No Product on platfrom")
                weightconfirm = 0
        except Exception as e:
            print(e)
            pass
if __name__ == '__main__':
    aoimodel=tf.keras.models.load_model("aoimodel.h5")
    agent=Process_line_agent(aoimodel=aoimodel)
    agent.connect()
    processlinereset()
    weightmeterreset()
    workflow()

    # processlinereset()
    # processlinemove()
