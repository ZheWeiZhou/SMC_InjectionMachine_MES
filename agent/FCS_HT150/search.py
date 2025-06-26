from opcua import Client
from opcua.ua import NodeClass
import traceback
from pprint import pprint
import time 
# OPC UA server endpoint（替換成你的機台網址）
url = "opc.tcp://192.168.1.12:4842"
worker = Client(url)
worker.connect()
print('Connect !!!')
injection_singal = worker.get_node("ns=4;s=APPL.Injection1.do_Inject").get_value()

processactivate = False
pressurecurve = []
speedcurve = []
while True:
    
    injection_singal = worker.get_node("ns=4;s=APPL.Injection1.do_Inject").get_value()
    if injection_singal is not False:
        processactivate = True
        actspeed = worker.get_node("ns=4;s=APPL.Injection1.sv_rScrewVelocityAbs").get_value()
        speedcurve.append(actspeed)
        actpressure = worker.get_node("ns=4;s=APPL.Injection1.ai_Pressure").get_value()*25.12
        pressurecurve.append(actpressure)
    else:
        if processactivate is True:
            print('Activate Process Finish')
            processactivate = False
            print(f'pressurecurve : {pressurecurve}')
            print('***********')
            print(f'SpeedCure {speedcurve}')
            pressurecurve = []
            speedcurve = []

worker.disconnect()

# try:
    
#     print("Connected to OPC UA Server")
#     starting_node_id = "ns=4;s=APPL.Mold1"
#     starting_node = worker.get_node(starting_node_id)
#     barrel_temp_set = {}
#     barrel_temp1_set                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain1.rSetValVis").get_value()
#     barrel_temp_set["barrel_temp1_set"]   = {"value":barrel_temp1_set,"edit":"none"}
#     barrel_temp2_set                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain2.rSetValVis").get_value()
#     barrel_temp_set["barrel_temp2_set"]   = {"value":barrel_temp2_set,"edit":"none"}
#     barrel_temp3_set                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain3.rSetValVis").get_value()
#     barrel_temp_set["barrel_temp3_set"]   = {"value":barrel_temp3_set,"edit":"none"}
#     barrel_temp4_set                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.sv_ZoneRetain4.rSetValVis").get_value()
#     barrel_temp_set["barrel_temp4_set"]   = {"value":barrel_temp4_set,"edit":"none"}
#     barrel_temp_real = {}
#     barrel_temp1_real                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp1").get_value()
#     barrel_temp_real["barrel_temp1_real"]  = {"value":barrel_temp1_real,"edit":"none"}
#     barrel_temp2_real                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp2").get_value()
#     barrel_temp_real["barrel_temp2_real"]  = {"value":barrel_temp2_real,"edit":"none"}
#     barrel_temp3_real                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp3").get_value()
#     barrel_temp_real["barrel_temp3_real"]  = {"value":barrel_temp3_real,"edit":"none"}
#     barrel_temp4_real                      = worker.get_node("ns=4;s=APPL.HeatingNozzle1.ti_InTemp4").get_value()
#     barrel_temp_real["barrel_temp4_real"]  = {"value":barrel_temp4_real,"edit":"none"}
#     pprint(barrel_temp_set)
#     pprint(barrel_temp_real)
#     holdingtimeset = {}
#     holding_time1_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rStartPos").get_value()
#     holdingtimeset["holding_time1_set"]     = {"value":holding_time1_set,"edit":"acctivate"}
#     holding_time2_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rStartPos").get_value()
#     holdingtimeset["holding_time2_set"]     = {"value":holding_time2_set,"edit":"acctivate"}
#     holding_time3_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rStartPos").get_value()
#     holdingtimeset["holding_time3_set"]     = {"value":holding_time3_set,"edit":"acctivate"}
#     holding_time4_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rStartPos").get_value()
#     holdingtimeset["holding_time4_set"]     = {"value":holding_time4_set,"edit":"acctivate"}
#     holding_time5_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rStartPos").get_value()
#     holdingtimeset["holding_time5_set"]     = {"value":holding_time5_set,"edit":"acctivate"}
#     holding_time6_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rStartPos").get_value()
#     holdingtimeset["holding_time6_set"]     = {"value":holding_time6_set,"edit":"acctivate"}
#     holding_time7_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rStartPos").get_value()
#     holdingtimeset["holding_time7_set"]     = {"value":holding_time7_set,"edit":"acctivate"}
#     holding_time8_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rStartPos").get_value()
#     holdingtimeset["holding_time8_set"]     = {"value":holding_time8_set,"edit":"acctivate"}
#     holding_time9_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rStartPos").get_value()
#     holdingtimeset["holding_time9_set"]     = {"value":holding_time9_set,"edit":"acctivate"}
#     pprint(holdingtimeset)
#     holdingpressureset ={}
#     holding_pressure1_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[1].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure1_set"] = {"value":holding_pressure1_set,"edit":"acctivate"}
#     holding_pressure2_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[2].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure2_set"] = {"value":holding_pressure2_set,"edit":"acctivate"}
#     holding_pressure3_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[3].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure3_set"] = {"value":holding_pressure3_set,"edit":"acctivate"}
#     holding_pressure4_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[4].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure4_set"] = {"value":holding_pressure4_set,"edit":"acctivate"}
#     holding_pressure5_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[5].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure5_set"] = {"value":holding_pressure5_set,"edit":"acctivate"}
#     holding_pressure6_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[6].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure6_set"] = {"value":holding_pressure6_set,"edit":"acctivate"}
#     holding_pressure7_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[7].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure7_set"] = {"value":holding_pressure7_set,"edit":"acctivate"}
#     holding_pressure8_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[8].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure8_set"] = {"value":holding_pressure8_set,"edit":"acctivate"}
#     holding_pressure9_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[9].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure9_set"] = {"value":holding_pressure9_set,"edit":"acctivate"}
#     holding_pressure10_set                       = worker.get_node("ns=4;s=APPL.Injection1.sv_HoldProfVis.Profile.Points[10].rPressure").get_value()/13.05
#     holdingpressureset["holding_pressure10_set"] = {"value":holding_pressure10_set,"edit":"acctivate"}
#     pprint(holdingpressureset)
#     injection_pos ={}
#     injection_volume1                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[2].rStartPos").get_value()/1.52
#     injection_pos["injection_volume1"]     = {"value":injection_volume1,"edit":"acctivate"}
#     injection_volume2                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[3].rStartPos").get_value()/1.52
#     injection_pos["injection_volume2"]     = {"value":injection_volume2,"edit":"acctivate"}
#     injection_volume3                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[4].rStartPos").get_value()/1.52
#     injection_pos["injection_volume3"]     = {"value":injection_volume3,"edit":"acctivate"}
#     injection_volume4                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[5].rStartPos").get_value()/1.52
#     injection_pos["injection_volume4"]     = {"value":injection_volume4,"edit":"acctivate"}
#     injection_volume5                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[6].rStartPos").get_value()/1.52
#     injection_pos["injection_volume5"]     = {"value":injection_volume5,"edit":"acctivate"}
#     injection_volume6                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[7].rStartPos").get_value()/1.52
#     injection_pos["injection_volume6"]     = {"value":injection_volume6,"edit":"acctivate"}
#     injection_volume7                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[8].rStartPos").get_value()/1.52
#     injection_pos["injection_volume7"]     = {"value":injection_volume7,"edit":"acctivate"}
#     injection_volume8                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[9].rStartPos").get_value()/1.52
#     injection_pos["injection_volume8"]     = {"value":injection_volume8,"edit":"acctivate"}
#     injection_volume9                      = worker.get_node("ns=4;s=APPL.Injection1.sv_InjectProfVis.Profile.Points[10].rStartPos").get_value()/1.52
#     injection_pos["injection_volume9"]     = {"value":injection_volume9,"edit":"acctivate"}
#     pprint(injection_pos)
# except Exception as e:
#     print("Error:", e)
# finally:
#     worker.disconnect()
#     print("Disconnected from server")