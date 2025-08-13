from opcua import Client
from opcua import ua

url      = "opc.tcp://192.168.1.11:4840"
worker   = Client(url)
worker.connect()
# temp1set = worker.get_node("ns=1;i=85131264").get_value()
# temp2set = worker.get_node("ns=1;i=85131265").get_value()
# temp3set = worker.get_node("ns=1;i=85131266").get_value()
# temp4set = worker.get_node("ns=1;i=85131267").get_value()
# temp5set = worker.get_node("ns=1;i=85131268").get_value()
# temp6set = worker.get_node("ns=1;i=85131269").get_value()
# temp7set = worker.get_node("ns=1;i=85131270").get_value()

# temp1real = worker.get_node("ns=1;i=85327875").get_value()
# temp2real = worker.get_node("ns=1;i=85327876").get_value()
# temp3real = worker.get_node("ns=1;i=85327877").get_value()
# temp4real = worker.get_node("ns=1;i=85327878").get_value()
# temp5real = worker.get_node("ns=1;i=85327879").get_value()
# temp6real = worker.get_node("ns=1;i=85327880").get_value()
# temp7real = worker.get_node("ns=1;i=85327881").get_value()


# vp_pos_set = worker.get_node("ns=1;i=269680644").get_value()/100
# storepos   = worker.get_node("ns=1;i=269877251").get_value()/100
# ijposset1  = worker.get_node("ns=1;i=269746236").get_value()/100
# ijposset2  = worker.get_node("ns=1;i=269746237").get_value()/100
# ijposset3  = worker.get_node("ns=1;i=269746238").get_value()/100
# ijposset4  = worker.get_node("ns=1;i=269746239").get_value()/100

# vp_realpre = worker.get_node("ns=1;i=269877255").get_value()
# vp_realspe = worker.get_node("ns=1;i=269877264").get_value()

# speedset1 = worker.get_node("ns=1;i=269746196").get_value()/10
# speedset2 = worker.get_node("ns=1;i=269746197").get_value()/10
# speedset3 = worker.get_node("ns=1;i=269746198").get_value()/10
# speedset4 = worker.get_node("ns=1;i=269746199").get_value()/10
# speedset5 = worker.get_node("ns=1;i=269746200").get_value()/10

# pressureset1 = worker.get_node("ns=1;i=269746176").get_value()
# pressureset2 = worker.get_node("ns=1;i=269746177").get_value()
# pressureset3 = worker.get_node("ns=1;i=269746178").get_value()
# pressureset4 = worker.get_node("ns=1;i=269746179").get_value()
# pressureset5 = worker.get_node("ns=1;i=269746180").get_value()

# injectionseg   = worker.get_node("ns=1;i=269680647").get_value()
# fillingtimeset = worker.get_node("ns=1;i=269680646").get_value()
# maxspeed       = worker.get_node("ns=1;i=269877324").get_value()
# maxijpre       = worker.get_node("ns=1;i=269877268").get_value()
# maxholdpre     = worker.get_node("ns=1;i=269877269").get_value()

# holdseg = worker.get_node("ns=1;i=269680649").get_value()

# holdpreset1 = worker.get_node("ns=1;i=269746186").get_value()
# holdpreset2 = worker.get_node("ns=1;i=269746187").get_value()
# holdpreset3 = worker.get_node("ns=1;i=269746188").get_value()
# holdpreset4 = worker.get_node("ns=1;i=269746189").get_value()

# holdtimeset1 = worker.get_node("ns=1;i=269746226").get_value()/100
# holdtimeset2 = worker.get_node("ns=1;i=269746227").get_value()/100
# holdtimeset3 = worker.get_node("ns=1;i=269746228").get_value()/100
# holdtimeset4 = worker.get_node("ns=1;i=269746229").get_value()/100

# holdtimespeed1 = worker.get_node("ns=1;i=269746206").get_value()/10
# holdtimespeed2 = worker.get_node("ns=1;i=269746207").get_value()/10
# holdtimespeed3 = worker.get_node("ns=1;i=269746208").get_value()/10
# holdtimespeed4 = worker.get_node("ns=1;i=269746209").get_value()/10

# screwrealpos = worker.get_node("ns=1;i=118882330").get_value()
# print(f'screw real pos {screwrealpos}')
# endpos = worker.get_node("ns=1;i=269877252").get_value()/100
# print(f'Injection end POS {endpos}')


# coolingtime = worker.get_node("ns=1;i=286457857").get_value()/100
import time 
from pprint import pprint
try:
    while True:
        item = {
            "injection_start_sign": worker.get_node("ns=1;i=269877271").get_value(),
            "injection_state_real": worker.get_node("ns=1;i=4279238725").get_value(),
            "operate_state":worker.get_node("ns=1;i=1441794").get_value(),
            "max_speed": worker.get_node("ns=1;i=269877324").get_value(),
            "cycle_time":  worker.get_node("ns=1;i=1441832").get_value(),
            "inj_time":  worker.get_node("ns=1;i=269877250").get_value(),
        }

        pprint(item)
        time.sleep(0.1)
finally:
    worker.disconnect()

# from opcua.ua.uaerrors import BadNoData
# def browse_and_print(node, level=0):
#     try:
#         display_name = node.get_display_name().Text
#     except Exception:
#         display_name = "<No DisplayName>"

#     try:
#         value = node.get_value()
#     except BadNoData:
#         value = "<No Value>"
#     except Exception:
#         value = "<Error Reading Value>"

#     node_id = str(node.nodeid)
#     indent = "  " * level
#     print(f"NodeId: {node_id}, DisplayName: {display_name}, Value: {value}")

#     # 遞迴瀏覽子節點
#     try:
#         children = node.get_children()
#         for child in children:
#             browse_and_print(child, level + 1)
#     except Exception as e:
#         pass
# try:
#     root = worker.get_root_node()
#     browse_and_print(root)
# except Exception as e:
#     print('fai;')
# finally:
#     worker.disconnect()






'''
NodeId: NumericNodeId(ns=1;i=4279238665), DisplayName: Alarm1, Value: 1048834
NodeId: NumericNodeId(ns=1;i=4279238666), DisplayName: Alarm2, Value: 0
NodeId: NumericNodeId(ns=1;i=1441794), DisplayName: Operate State, Value: 9
NodeId: NumericNodeId(ns=1;i=85327875), DisplayName: Temp1 Real, Value: 205
NodeId: NumericNodeId(ns=1;i=85327876), DisplayName: Temp2 Real, Value: 210
NodeId: NumericNodeId(ns=1;i=85327877), DisplayName: Temp3 Real, Value: 205
NodeId: NumericNodeId(ns=1;i=85327878), DisplayName: Temp4 Real, Value: 200
NodeId: NumericNodeId(ns=1;i=85327879), DisplayName: Temp5 Real, Value: 195
NodeId: NumericNodeId(ns=1;i=85327880), DisplayName: Temp6 Real, Value: 0
NodeId: NumericNodeId(ns=1;i=85327881), DisplayName: Temp7 Real, Value: 0
NodeId: NumericNodeId(ns=1;i=85131264), DisplayName: Temp1 Set, Value: 205
NodeId: NumericNodeId(ns=1;i=85131265), DisplayName: Temp2 Set, Value: 210
NodeId: NumericNodeId(ns=1;i=85131266), DisplayName: Temp3 Set, Value: 205
NodeId: NumericNodeId(ns=1;i=85131267), DisplayName: Temp4 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=85131268), DisplayName: Temp5 Set, Value: 195
NodeId: NumericNodeId(ns=1;i=85131269), DisplayName: Temp6 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=85131270), DisplayName: Temp7 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=269746176), DisplayName: InjPrs#1 Set, Value: 1275
NodeId: NumericNodeId(ns=1;i=269746177), DisplayName: InjPrs#2 Set, Value: 1200
NodeId: NumericNodeId(ns=1;i=269746178), DisplayName: InjPrs#3 Set, Value: 1350
NodeId: NumericNodeId(ns=1;i=269746179), DisplayName: InjPrs#4 Set, Value: 1245
NodeId: NumericNodeId(ns=1;i=269746180), DisplayName: InjPrs#5 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746186), DisplayName: HoldPrs#1 Set, Value: 500
NodeId: NumericNodeId(ns=1;i=269746187), DisplayName: HoldPrs#2 Set, Value: 734
NodeId: NumericNodeId(ns=1;i=269746188), DisplayName: HoldPrs#3 Set, Value: 408
NodeId: NumericNodeId(ns=1;i=269746189), DisplayName: HoldPrs#4 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746196), DisplayName: InjSpd#1 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746197), DisplayName: InjSpd#2 Set, Value: 80
NodeId: NumericNodeId(ns=1;i=269746198), DisplayName: InjSpd#3 Set, Value: 239
NodeId: NumericNodeId(ns=1;i=269746199), DisplayName: InjSpd#4 Set, Value: 143
NodeId: NumericNodeId(ns=1;i=269746200), DisplayName: InjSpd#5 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746206), DisplayName: HoldSpd#1 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746207), DisplayName: HoldSpd#2 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746208), DisplayName: HoldSpd#3 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746209), DisplayName: HoldSpd#4 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269680646), DisplayName: InjTm Set, Value: 700
NodeId: NumericNodeId(ns=1;i=269746226), DisplayName: HoldTm#1 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746227), DisplayName: HoldTm#2 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746228), DisplayName: HoldTm#3 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746229), DisplayName: HoldTm#4 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746236), DisplayName: InjEndPos#1 Set, Value: 1450
NodeId: NumericNodeId(ns=1;i=269746237), DisplayName: InjEndPos#2 Set, Value: 1295
NodeId: NumericNodeId(ns=1;i=269746238), DisplayName: InjEndPos#3 Set, Value: 1061
NodeId: NumericNodeId(ns=1;i=269746239), DisplayName: InjEndPos#4 Set, Value: 1015
NodeId: NumericNodeId(ns=1;i=269680644), DisplayName: TurnHoldPos Set, Value: 800
NodeId: NumericNodeId(ns=1;i=269746246), DisplayName: ChargeBackPrs#1 Set, Value: 20
NodeId: NumericNodeId(ns=1;i=269746247), DisplayName: ChargeBackPrs#2 Set, Value: 20
NodeId: NumericNodeId(ns=1;i=269746248), DisplayName: ChargeBackPrs#3 Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269746251), DisplayName: ChargeSpd#1 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746252), DisplayName: ChargeSpd#2 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=269746253), DisplayName: ChargeSpd#3 Set, Value: 150
NodeId: NumericNodeId(ns=1;i=269746256), DisplayName: ChargeEndPos#1 Set, Value: 1000
NodeId: NumericNodeId(ns=1;i=269746257), DisplayName: ChargeEndPos#2 Set, Value: 1500
NodeId: NumericNodeId(ns=1;i=269746258), DisplayName: ChargeEndPos#3 Set, Value: 10000
NodeId: NumericNodeId(ns=1;i=269746261), DisplayName: SuckBackSpd Set, Value: 261
NodeId: NumericNodeId(ns=1;i=269746263), DisplayName: SuckBackDistance Set, Value: 665
NodeId: NumericNodeId(ns=1;i=538181637), DisplayName: CloseSpd#1 Set, Value: 300
NodeId: NumericNodeId(ns=1;i=538181638), DisplayName: CloseSpd#2 Set, Value: 800
NodeId: NumericNodeId(ns=1;i=538181639), DisplayName: CloseSpd#3 Set, Value: 500
NodeId: NumericNodeId(ns=1;i=538181640), DisplayName: CloseLowSpd Set, Value: 300
NodeId: NumericNodeId(ns=1;i=538181641), DisplayName: CloseHiSpd Set, Value: 200
NodeId: NumericNodeId(ns=1;i=538181642), DisplayName: ClosePos#1 Set, Value: 33300
NodeId: NumericNodeId(ns=1;i=538181643), DisplayName: ClosePos#2 Set, Value: 5000
NodeId: NumericNodeId(ns=1;i=538181644), DisplayName: ClosePos#3 Set, Value: 1200
NodeId: NumericNodeId(ns=1;i=538181645), DisplayName: CloseLowPos Set, Value: 200
NodeId: NumericNodeId(ns=1;i=538181651), DisplayName: OpenSpd#1 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=538181652), DisplayName: OpenSpd#2 Set, Value: 500
NodeId: NumericNodeId(ns=1;i=538181653), DisplayName: OpenSpd#3 Set, Value: 800
NodeId: NumericNodeId(ns=1;i=538181654), DisplayName: OpenSpd#4 Set, Value: 660
NodeId: NumericNodeId(ns=1;i=538181655), DisplayName: OpenSpdEnd Set, Value: 200
NodeId: NumericNodeId(ns=1;i=538181656), DisplayName: OpenPos#1 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=538181657), DisplayName: OpenPos#2 Set, Value: 25000
NodeId: NumericNodeId(ns=1;i=538181658), DisplayName: OpenPos#3 Set, Value: 30000
NodeId: NumericNodeId(ns=1;i=538181659), DisplayName: OpenPos#4 Set, Value: 32500
NodeId: NumericNodeId(ns=1;i=538181660), DisplayName: OpenPosEnd Set, Value: 30000
NodeId: NumericNodeId(ns=1;i=554958853), DisplayName: EjtAdvSpd#1 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=554958854), DisplayName: EjtAdvSpd#2 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=554958855), DisplayName: EjtRetSpd#1 Set, Value: 200
NodeId: NumericNodeId(ns=1;i=554958856), DisplayName: EjtRetSpd#2 Set, Value: 100
NodeId: NumericNodeId(ns=1;i=554958857), DisplayName: EjtAdvPos#1 Set, Value: 2000
NodeId: NumericNodeId(ns=1;i=554958858), DisplayName: EjtAdvPos#2 Set, Value: 5000
NodeId: NumericNodeId(ns=1;i=554958859), DisplayName: EjtRetPos#1 Set, Value: 1000
NodeId: NumericNodeId(ns=1;i=554958860), DisplayName: EjtRetPos#2 Set, Value: 10
NodeId: NumericNodeId(ns=1;i=1441801), DisplayName: ProdTm Real, Value: 241
NodeId: NumericNodeId(ns=1;i=269877250), DisplayName: Inj Tm Real, Value: 146
NodeId: NumericNodeId(ns=1;i=269877251), DisplayName: InjStartPos Real, Value: 2000
NodeId: NumericNodeId(ns=1;i=269877253), DisplayName: HoldStartPos Real, Value: 774
NodeId: NumericNodeId(ns=1;i=269877252), DisplayName: RestmillPos Real, Value: 598
NodeId: NumericNodeId(ns=1;i=269877261), DisplayName: Charge Pos Real, Value: 1500
NodeId: NumericNodeId(ns=1;i=269877258), DisplayName: Charge Tm Real, Value: 96
NodeId: NumericNodeId(ns=1;i=538312711), DisplayName: Close Tm Real, Value: 0
NodeId: NumericNodeId(ns=1;i=538312713), DisplayName: CloseLowPrs Tm Real, Value: 226
NodeId: NumericNodeId(ns=1;i=538312715), DisplayName: CloseHiPrs Tm Real, Value: 2
NodeId: NumericNodeId(ns=1;i=538312718), DisplayName: Open Tm Real, Value: 172
NodeId: NumericNodeId(ns=1;i=538312717), DisplayName: Open EndPos Real, Value: 29999
NodeId: NumericNodeId(ns=1;i=269877255), DisplayName: TurnHold Prs Real, Value: 420
NodeId: NumericNodeId(ns=1;i=269877264), DisplayName: TurnHold Spd Real, Value: 95
NodeId: NumericNodeId(ns=1;i=269877262), DisplayName: SuckBack Time Real, Value: 34
NodeId: NumericNodeId(ns=1;i=269877265), DisplayName: SuckBack EndPos Real, Value: 2000
NodeId: NumericNodeId(ns=1;i=555089922), DisplayName: Eject Tm Real, Value: 296
NodeId: NumericNodeId(ns=1;i=286654466), DisplayName: NozAdv Tm Real, Value: 991
NodeId: NumericNodeId(ns=1;i=286654467), DisplayName: NozRet Tm Real, Value: 0
NodeId: NumericNodeId(ns=1;i=269877267), DisplayName: Inj Avg Spd Real, Value: 838
NodeId: NumericNodeId(ns=1;i=269877268), DisplayName: Max InjPrs Real, Value: 420
NodeId: NumericNodeId(ns=1;i=269877269), DisplayName: Max HoldPrs Real, Value: 528
NodeId: NumericNodeId(ns=1;i=269877270), DisplayName: Hold MoveDist Real, Value: 176
NodeId: NumericNodeId(ns=1;i=538312706), DisplayName: OpenCnt Hi Real, Value: 0
NodeId: NumericNodeId(ns=1;i=538312707), DisplayName: OpenCnt Low Real, Value: 2154
NodeId: NumericNodeId(ns=1;i=1441832), DisplayName: CycTime Real, Value: 254
NodeId: NumericNodeId(ns=1;i=555089931), DisplayName: Eject End Pos, Value: 5000
NodeId: NumericNodeId(ns=1;i=269877324), DisplayName: Inject Max Speed, Value: 104
NodeId: NumericNodeId(ns=1;i=269877274), DisplayName: Inject Min Pos, Value: 594
NodeId: NumericNodeId(ns=1;i=538116099), DisplayName: Close Segments Set, Value: 3
NodeId: NumericNodeId(ns=1;i=538116114), DisplayName: HiPrsLockProtTm Set, Value: 9000
NodeId: NumericNodeId(ns=1;i=538116105), DisplayName: Open Segments Set, Value: 3
NodeId: NumericNodeId(ns=1;i=554893321), DisplayName: EjeAdv Segments Set, Value: 2
NodeId: NumericNodeId(ns=1;i=554893314), DisplayName: Eject Mode Set, Value: 3
NodeId: NumericNodeId(ns=1;i=554893312), DisplayName: Dly Before EjectAdv Set, Value: 0
NodeId: NumericNodeId(ns=1;i=554827790), DisplayName: Dly After EjectAdv Set, Value: 0
NodeId: NumericNodeId(ns=1;i=554893322), DisplayName: EjeRet Segments Set, Value: 2
NodeId: NumericNodeId(ns=1;i=554893313), DisplayName: Dly Before EjectRet Set, Value: 0
NodeId: NumericNodeId(ns=1;i=554827791), DisplayName: Dly After EjectRet Set, Value: 0
NodeId: NumericNodeId(ns=1;i=269680647), DisplayName: Inject Segments Set, Value: 2
NodeId: NumericNodeId(ns=1;i=286457859), DisplayName: Cool TimeH Set, Value: 0
NodeId: NumericNodeId(ns=1;i=286457857), DisplayName: Cool TimeL Set, Value: 700
NodeId: NumericNodeId(ns=1;i=269680649), DisplayName: Hold Segments Set, Value: 1
NodeId: NumericNodeId(ns=1;i=269680648), DisplayName: Charge Segments Set, Value: 2
NodeId: NumericNodeId(ns=1;i=269746280), DisplayName: ChargePrs#1 Set, Value: 1000
NodeId: NumericNodeId(ns=1;i=269746281), DisplayName: ChargePrs#2 Set, Value: 1000
NodeId: NumericNodeId(ns=1;i=269746282), DisplayName: ChargePrs#3 Set, Value: 1500
NodeId: NumericNodeId(ns=1;i=269746262), DisplayName: Charge After InjSpd Set, Value: 200
NodeId: NumericNodeId(ns=1;i=269746264), DisplayName: Charge After InjPos Set, Value: 500
NodeId: NumericNodeId(ns=1;i=571670529), DisplayName: Core A Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=571736064), DisplayName: Core A In Prs Set, Value: 60
NodeId: NumericNodeId(ns=1;i=571736065), DisplayName: Core A Out Prs Set, Value: 60
NodeId: NumericNodeId(ns=1;i=571736066), DisplayName: Core A In Spd Set, Value: 30
NodeId: NumericNodeId(ns=1;i=571736067), DisplayName: Core A Out Spd Set, Value: 30
NodeId: NumericNodeId(ns=1;i=571736068), DisplayName: Core A In Tm Set, Value: 20
NodeId: NumericNodeId(ns=1;i=571736069), DisplayName: Core A Out Tm Set, Value: 20
NodeId: NumericNodeId(ns=1;i=572719105), DisplayName: Core B Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=572784640), DisplayName: Core B In Prs Set, Value: 50
NodeId: NumericNodeId(ns=1;i=572784641), DisplayName: Core B Out Prs Set, Value: 45
NodeId: NumericNodeId(ns=1;i=572784642), DisplayName: Core B In Spd Set, Value: 50
NodeId: NumericNodeId(ns=1;i=572784643), DisplayName: Core B Out Spd Set, Value: 45
NodeId: NumericNodeId(ns=1;i=572784644), DisplayName: Core B In Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=572784645), DisplayName: Core B Out Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=573767681), DisplayName: Core C Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=573833216), DisplayName: Core C In Prs Set, Value: 50
NodeId: NumericNodeId(ns=1;i=573833217), DisplayName: Core C Out Prs Set, Value: 45
NodeId: NumericNodeId(ns=1;i=573833218), DisplayName: Core C In Spd Set, Value: 50
NodeId: NumericNodeId(ns=1;i=573833219), DisplayName: Core C Out Spd Set, Value: 45
NodeId: NumericNodeId(ns=1;i=573833220), DisplayName: Core C In Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=573833221), DisplayName: Core C Out Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=574816257), DisplayName: Core D Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=574881792), DisplayName: Core D In Prs Set, Value: 50
NodeId: NumericNodeId(ns=1;i=574881793), DisplayName: Core D Out Prs Set, Value: 45
NodeId: NumericNodeId(ns=1;i=574881794), DisplayName: Core D In Spd Set, Value: 50
NodeId: NumericNodeId(ns=1;i=574881795), DisplayName: Core D Out Spd Set, Value: 45
NodeId: NumericNodeId(ns=1;i=574881796), DisplayName: Core D In Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=574881797), DisplayName: Core D Out Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=575864833), DisplayName: Core E Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=575930368), DisplayName: Core E In Prs Set, Value: 50
NodeId: NumericNodeId(ns=1;i=575930369), DisplayName: Core E Out Prs Set, Value: 45
NodeId: NumericNodeId(ns=1;i=575930370), DisplayName: Core E In Spd Set, Value: 50
NodeId: NumericNodeId(ns=1;i=575930371), DisplayName: Core E Out Spd Set, Value: 45
NodeId: NumericNodeId(ns=1;i=575930372), DisplayName: Core E In Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=575930373), DisplayName: Core E Out Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=576913409), DisplayName: Core F Use Set, Value: 0
NodeId: NumericNodeId(ns=1;i=576978944), DisplayName: Core F In Prs Set, Value: 50
NodeId: NumericNodeId(ns=1;i=576978945), DisplayName: Core F Out Prs Set, Value: 45
NodeId: NumericNodeId(ns=1;i=576978946), DisplayName: Core F In Spd Set, Value: 50
NodeId: NumericNodeId(ns=1;i=576978947), DisplayName: Core F Out Spd Set, Value: 45
NodeId: NumericNodeId(ns=1;i=576978948), DisplayName: Core F In Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=576978949), DisplayName: Core F Out Tm Set, Value: 30
NodeId: NumericNodeId(ns=1;i=605159442), DisplayName: Close Lock Press, Value: 800
NodeId: NumericNodeId(ns=1;i=118882368), DisplayName: InjPrs Sensor Real, Value: 12
NodeId: NumericNodeId(ns=1;i=840040474), DisplayName: bMESsetUpdate, Value: 0
NodeId: NumericNodeId(ns=1;i=840040475), DisplayName: rWrite_back, Value: 0
NodeId: NumericNodeId(ns=1;i=840040476), DisplayName: rConfirm, Value: 0
NodeId: NumericNodeId(ns=1;i=840040477), DisplayName: rMaterial, Value: 36
NodeId: NumericNodeId(ns=1;i=840040478), DisplayName: rmethod, Value: 1
NodeId: NumericNodeId(ns=1;i=840040479), DisplayName: rCavities_Member, Value: 1
NodeId: NumericNodeId(ns=1;i=840040480), DisplayName: rRunner_volume, Value: 1000
NodeId: NumericNodeId(ns=1;i=840040481), DisplayName: rProduct_volume, Value: 3000
NodeId: NumericNodeId(ns=1;i=840040482), DisplayName: rProduct_length, Value: 1000
NodeId: NumericNodeId(ns=1;i=840040483), DisplayName: rProduct_width, Value: 100
NodeId: NumericNodeId(ns=1;i=840040484), DisplayName: rProduct_height, Value: 20
NodeId: NumericNodeId(ns=1;i=840040485), DisplayName: rGate_thickness, Value: 10
NodeId: NumericNodeId(ns=1;i=840040486), DisplayName: rMax_thickness, Value: 12
NodeId: NumericNodeId(ns=1;i=840040487), DisplayName: rAverage_thickness, Value: 5
NodeId: NumericNodeId(ns=1;i=840040488), DisplayName: rLT_ratio, Value: 83
NodeId: NumericNodeId(ns=1;i=840040489), DisplayName: rProduct_type, Value: 3
NodeId: NumericNodeId(ns=1;i=840040490), DisplayName: rGate_type, Value: 1
NodeId: NumericNodeId(ns=1;i=840040491), DisplayName: rAppearance, Value: 3
NodeId: NumericNodeId(ns=1;i=840040492), DisplayName: rCoolingdesign, Value: 1
NodeId: NumericNodeId(ns=1;i=840040493), DisplayName: rAppearance_type, Value: 1
NodeId: NumericNodeId(ns=1;i=840040494), DisplayName: rWarping_type, Value: 0
NodeId: NumericNodeId(ns=1;i=840040495), DisplayName: rGate_issues, Value: 0
NodeId: NumericNodeId(ns=1;i=840040496), DisplayName: rSize_type, Value: 0
NodeId: NumericNodeId(ns=1;i=840040497), DisplayName: rWeight, Value: 0
NodeId: NumericNodeId(ns=1;i=840040498), DisplayName: rOther, Value: 0
NodeId: NumericNodeId(ns=1;i=840040499), DisplayName: rParameter, Value: 0
NodeId: NumericNodeId(ns=1;i=4279238725), DisplayName: Inject State Real, Value: 0
NodeId: NumericNodeId(ns=1;i=4244635931), DisplayName: AdaptiveControl Para, Value: 1
NodeId: NumericNodeId(ns=1;i=4244635932), DisplayName: HoldPrs Amend Range, Value: 200
NodeId: NumericNodeId(ns=1;i=4244635933), DisplayName: VPPos Amend Range, Value: 2
NodeId: NumericNodeId(ns=1;i=4244635934), DisplayName: Mold Cavity Num, Value: 1
NodeId: NumericNodeId(ns=1;i=4244635935), DisplayName: Work Order Num, Value: 2000
NodeId: NumericNodeId(ns=1;i=4279238727), DisplayName: Total Num, Value: 0
NodeId: NumericNodeId(ns=1;i=4279238726), DisplayName: Btn Start, Value: 0
NodeId: NumericNodeId(ns=1;i=4279238731), DisplayName: Robot Control, Value: 0
NodeId: NumericNodeId(ns=1;i=4279238729), DisplayName: Machine Alarm, Value: 0
NodeId: NumericNodeId(ns=1;i=4279238728), DisplayName: Train State, Value: 0
NodeId: NumericNodeId(ns=1;i=269877271), DisplayName: Inject Strat Sign, Value: 65026
NodeId: NumericNodeId(ns=1;i=118882330), DisplayName: Inject Real Pos, Value: 2000
NodeId: FourByteNodeId(ns=1;i=4096), DisplayName: Lv0.Everyone, Value: 0
NodeId: FourByteNodeId(ns=1;i=4097), DisplayName: Lv1.Adjuster, Value: 5858
NodeId: FourByteNodeId(ns=1;i=4098), DisplayName: Lv2.TeamLeader, Value: 7474
NodeId: FourByteNodeId(ns=1;i=4099), DisplayName: Lv3.Manager, Value: 5959
'''

