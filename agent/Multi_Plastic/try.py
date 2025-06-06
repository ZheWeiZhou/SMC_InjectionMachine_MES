from pycomm3 import LogixDriver

# # 連接 NJ 控制器 IP，指定槽位 0
with LogixDriver('192.168.250.3') as plc:
    value = plc.read('SP_IN_HMI')
    print('讀到的值:', value.value)


# from fins.tcp import TCPFinsConnection

# conn = TCPFinsConnection()      # 不帶參數初始化
# conn.connect('192.168.250.3')  # 呼叫 connect 時傳入IP

# data = conn.memory_area_read('DM', bytes([0, 0, 10]), 10)
# print(data)

# # conn.memory_area_write('DM', 0, [123, 456])

# conn.close()
