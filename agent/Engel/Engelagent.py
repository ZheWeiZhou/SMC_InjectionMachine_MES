from opcua import Client
from opcua import ua
import redis
import numpy as np
from datetime import datetime
import os
import json
class engelagent:
    def __init__(self,machineaddress,user,password,machineid):
        self.machineid = machineid
        self.machineaddress = machineaddress
        self.user = user
        self.password = password
        self.processactivate = False
        self.worker = ""
        self.red = redis.Redis(host='localhost',port=6379,db=0)
        self.actpressurecurve = []
        self.actspeedcurve = []
        self.motorpower = []
        self.heaterpower= []
        self.screwposition = []
        self.timeindex = []
        self.machinestatus   = {}
        self.machinefeedback = {}
        self.machinecurve   = {}
        
    def connect(self):  
        url="opc.tcp://"+self.machineaddress
        self.worker=Client(url)
        try:
            self.worker.set_user(self.user)
            self.worker.set_password(self.password)
            self.worker.connect()
            print("[MESSAGE] Success connect to Engel")
        except:
            print("[ERROR] Connect to Engel fail")
    
    def productpredict(self,input):
        print("[MESSAGE] Start to predict product quality")
        modelinput=np.array([input])
        print(modelinput)
        normodelinput=self.normalize.transform(modelinput)
        print(f'Nor {normodelinput}')
        modelresponse=self.model.predict(normodelinput)[0]
        print(f"Model response{modelresponse}")
        if modelresponse >0.5:
            modelresponse=1
            ProductQ="ng"
        else:
            modelresponse=0
            ProductQ="good"
        self.red.set('ProductQ',ProductQ)
        self.red.set('nglevel',str(modelresponse))
        print(f'[Message] model predict response: {modelresponse}')
    def collectdata(self):
        # Check processstatus
        processstatus                      = self.worker.get_node("ns=1;i=77").get_value()
        # barrel temp
        barrel_temp1_set                   = self.worker.get_node("ns=1;i=164").get_value()
        self.machinestatus["barrel_temp1_set"]  = barrel_temp1_set
        barrel_temp1_real                  = self.worker.get_node("ns=1;i=173").get_value()
        self.machinestatus["barrel_temp1_real"] = barrel_temp1_real
        barrel_temp2_set                   = self.worker.get_node("ns=1;i=220").get_value()
        self.machinestatus["barrel_temp2_set"]  = barrel_temp2_set
        barrel_temp2_real                  = self.worker.get_node("ns=1;i=229").get_value()
        self.machinestatus["barrel_temp2_real"] = barrel_temp2_real
        barrel_temp3_set                   = self.worker.get_node("ns=1;i=276").get_value()
        self.machinestatus["barrel_temp3_set"]  = barrel_temp3_set
        barrel_temp3_real                  = self.worker.get_node("ns=1;i=285").get_value()
        self.machinestatus["barrel_temp3_real"] = barrel_temp3_real
        barrel_temp4_set                   = self.worker.get_node("ns=1;i=332").get_value()
        self.machinestatus["barrel_temp4_set"]  = barrel_temp4_set
        barrel_temp4_real                  = self.worker.get_node("ns=1;i=341").get_value()
        self.machinestatus["barrel_temp4_real"] = barrel_temp4_real
        barrel_temp5_set                   = self.worker.get_node("ns=1;i=388").get_value()
        self.machinestatus["barrel_temp5_set"]  = barrel_temp5_set
        barrel_temp5_real                  = self.worker.get_node("ns=1;i=397").get_value()
        self.machinestatus["barrel_temp5_real"] = barrel_temp5_real
        barrel_temp6_set                   = self.worker.get_node("ns=1;i=444").get_value()
        self.machinestatus["barrel_temp6_set"]  = barrel_temp6_set
        barrel_temp6_real                  = self.worker.get_node("ns=1;i=453").get_value()
        self.machinestatus["barrel_temp6_real"] = barrel_temp6_real
        #Holding pressure & time setting
        holding_time1_set                      = self.worker.get_node("ns=5;i=57").get_value()
        self.machinestatus["holding_time1_set"]     = holding_time1_set
        holding_pressure1_set                  = self.worker.get_node("ns=5;i=52").get_value()
        self.machinestatus["holding_pressure1_set"] = holding_pressure1_set
        holding_time2_set                      = self.worker.get_node("ns=5;i=58").get_value()
        self.machinestatus["holding_time2_set"]     = holding_time2_set
        holding_pressure2_set                  = self.worker.get_node("ns=5;i=53").get_value()
        self.machinestatus["holding_pressure2_set"] = holding_pressure2_set
        holding_time3_set                      = self.worker.get_node("ns=5;i=59").get_value()
        self.machinestatus["holding_time3_set"]     = holding_time3_set
        holding_pressure3_set                  = self.worker.get_node("ns=5;i=54").get_value()
        self.machinestatus["holding_pressure3_set"] = holding_pressure3_set
        holding_time4_set                      = self.worker.get_node("ns=5;i=60").get_value()
        self.machinestatus["holding_time4_set"]     = holding_time4_set
        holding_pressure4_set                  = self.worker.get_node("ns=5;i=55").get_value()
        self.machinestatus["holding_pressure4_set"] = holding_pressure4_set
        #Injection volume(position) set
        injection_volume1                    = self.worker.get_node("ns=5;i=63").get_value()
        self.machinestatus["injection_volume1"]   = injection_volume1
        injection_volume2                    = self.worker.get_node("ns=5;i=48").get_value()
        self.machinestatus["injection_volume2"]   = injection_volume2
        injection_volume3                    = self.worker.get_node("ns=5;i=49").get_value()
        self.machinestatus["injection_volume3"]   = injection_volume3
        injection_volume4                    = self.worker.get_node("ns=5;i=50").get_value()
        self.machinestatus["injection_volume4"]   = injection_volume4
        injection_volume5                    = self.worker.get_node("ns=5;i=51").get_value()
        self.machinestatus["injection_volume5"]   = injection_volume5
        #Injection rate(speed) set
        injection_rate1_set                  = self.worker.get_node("ns=5;i=42").get_value()
        self.machinestatus["injection_rate1_set"] = injection_rate1_set
        injection_rate2_set                  = self.worker.get_node("ns=5;i=43").get_value()
        self.machinestatus["injection_rate2_set"] = injection_rate2_set
        injection_rate3_set                  = self.worker.get_node("ns=5;i=44").get_value()
        self.machinestatus["injection_rate3_set"] = injection_rate3_set
        injection_rate4_set                  = self.worker.get_node("ns=5;i=45").get_value()
        self.machinestatus["injection_rate4_set"] = injection_rate4_set
        injection_rate5_set                  = self.worker.get_node("ns=5;i=46").get_value()
        self.machinestatus["injection_rate5_set"] = injection_rate5_set

        #VP position setting
        vp_position_set                  = self.worker.get_node("ns=5;i=70").get_value()
        self.machinestatus["vp_position_set"] = vp_position_set
        #Cooling time
        cooling_time                     = self.worker.get_node("ns=5;i=62").get_value()
        self.machinestatus["cooling_time"]    = cooling_time
        #Injection pressure setting
        injection_pressure_set                     = self.worker.get_node("ns=5;i=69").get_value()
        self.machinestatus["injection_pressure_set"]    = injection_pressure_set
        #Back pressure
        backpressure1                     = self.worker.get_node("ns=5;i=71").get_value()
        self.machinestatus["backpressure1"]    = backpressure1
        backpressure2                     = self.worker.get_node("ns=5;i=72").get_value()
        self.machinestatus["backpressure2"]    = backpressure2
        backpressure3                     = self.worker.get_node("ns=5;i=73").get_value()
        self.machinestatus["backpressure3"]    = backpressure3
        # Material Cushion (餘料)
        material_cushion                  = self.worker.get_node("ns=5;i=82").get_value()
        self.machinestatus["material_cushion"] = material_cushion
        #Clamp force set
        clamp_force_set                   = self.worker.get_node("ns=5;i=85").get_value()
        self.machinestatus["clamp_force_set"]  = clamp_force_set

        if processstatus == 4:
            self.machinestatus['machine'] = 'work'
            self.processactivate=True
            # #Collect Realtime IJ presure
            actijpressure = self.worker.get_node("ns=5;i=114").get_value()
            self.actpressurecurve.append(actijpressure)
            # #Collect real time IJ speed
            actijspeed=self.worker.get_node("ns=5;i=115").get_value()
            self.actspeedcurve.append(actijspeed)
            # Get ACT motor power
            actmotorpower = self.worker.get_node("ns=5;i=118").get_value()
            self.motorpower.append(actmotorpower)
            #Get ACT heater power
            actheaterpower = self.worker.get_node("ns=5;i=120").get_value()
            self.heaterpower.append(actheaterpower)

            self.machinecurve["actpressurecurve"] = self.actpressurecurve
            self.machinecurve["actspeedcurve"]    = self.actspeedcurve
            self.machinecurve["motorpower"]       = self.motorpower
            self.machinecurve["heaterpower"]      = self.heaterpower



        else:
            self.machinestatus['machine'] = 'stay'
            if self.processactivate == True:
                print("[Message] Save data ...")
                # Screw volume
                screw_volume                    = self.worker.get_node("ns=1;i=126").get_value()
                self.machinefeedback["screw_volume"] = screw_volume
                #Filling time
                filling_time                    = self.worker.get_node("ns=5;i=75").get_value()
                self.machinefeedback["filling_time"] = filling_time
                #Maximun real injection pressure
                Maximun_real_injection_pressure                    = self.worker.get_node("ns=5;i=74").get_value()
                self.machinefeedback["Maximun_real_injection_pressure"] = Maximun_real_injection_pressure
                #Maximun real injection speed
                maximun_real_injection_speed                    = self.worker.get_node("ns=5;i=77").get_value()
                self.machinefeedback["maximun_real_injection_speed"] = maximun_real_injection_speed
                #Filling start position
                filling_start_position                    = self.worker.get_node("ns=4;i=6164").get_value()
                self.machinefeedback["filling_start_position"] = filling_start_position
                #VP position real
                vp_position_real                    = self.worker.get_node("ns=5;i=76").get_value()
                self.machinefeedback["vp_position_real"] = vp_position_real
                storage_position                    = self.worker.get_node("ns=5;i=63").get_value()
                self.machinefeedback["storage_position"] = storage_position
                #real vp pressure
                real_vp_pressure                    = self.worker.get_node("ns=5;i=78").get_value()
                self.machinefeedback["real_vp_pressure"] = real_vp_pressure
                #Act plastic time
                act_plastic_time                    = self.worker.get_node("ns=5;i=79").get_value()
                self.machinefeedback["act_plastic_time"] = act_plastic_time
                #Act cycle time
                act_cycle_time                    = self.worker.get_node("ns=5;i=83").get_value()
                self.machinefeedback["act_cycle_time"] = act_cycle_time
                #Maximun_screw_torque
                maximun_screw_torque                    = self.worker.get_node("ns=5;i=86").get_value()
                self.machinefeedback["maximun_screw_torque"] = maximun_screw_torque
                #Mean_screw_torque
                mean_screw_torque                    = self.worker.get_node("ns=5;i=87").get_value()
                self.machinefeedback["mean_screw_torque"] = mean_screw_torque
                # Motor Energy (KWH)
                motorenergy                    = self.worker.get_node("ns=5;i=122").get_value()
                self.machinefeedback["motorenergy"] = motorenergy
                # Heater Engery (KWH)
                heaterenergy                    = self.worker.get_node("ns=5;i=123").get_value()
                self.machinefeedback["heaterenergy"] = heaterenergy
                # Oil Motor Energy (KWH)
                Oilmotorenergy                    = self.worker.get_node("ns=5;i=124").get_value()
                self.machinefeedback["Oilmotorenergy"] = Oilmotorenergy
                # Injection Motor Energy (KWH)
                injectionmotorenergy                    = self.worker.get_node("ns=5;i=125").get_value()
                self.machinefeedback["injectionmotorenergy"] = injectionmotorenergy
                # Plastic Motor Energy (KWH)
                plasticmotorenergy                    = self.worker.get_node("ns=5;i=126").get_value()
                self.machinefeedback["plasticmotorenergy"] = plasticmotorenergy
                # Close Mold Energy (KWH)
                closemoldenergy                    = self.worker.get_node("ns=5;i=127").get_value()
                self.machinefeedback["closemoldenergy"] = closemoldenergy
                # Nozzle Energy
                nozzle_energy                    = self.worker.get_node("ns=5;i=128").get_value()
                self.machinefeedback["nozzle_energy"] = nozzle_energy
                # Injection Energy
                injection_energy                    = self.worker.get_node("ns=5;i=129").get_value()
                self.machinefeedback["injection_energy"] = injection_energy
                # Holding Energy
                holdingenergy                    = self.worker.get_node("ns=5;i=130").get_value()
                self.machinefeedback["holdingenergy"] = holdingenergy
                # Cooling Energy
                coolingenergy                    = self.worker.get_node("ns=5;i=131").get_value()
                self.machinefeedback["coolingenergy"] = coolingenergy
                # Plastic Energy
                plasticenergy                    = self.worker.get_node("ns=5;i=132").get_value()
                self.machinefeedback["plasticenergy"] = plasticenergy
                #Open mold energy
                openmoldenergy                    = self.worker.get_node("ns=5;i=133").get_value()
                self.machinefeedback["openmoldenergy"] = openmoldenergy
                #Eject energy
                ejectenergy                    = self.worker.get_node("ns=5;i=134").get_value()
                self.machinefeedback["ejectenergy"] = ejectenergy
                #semi auto energy
                semi_energy                    = self.worker.get_node("ns=5;i=135").get_value()
                self.machinefeedback["semi_energy"] = semi_energy
                # Core energy
                core_energy                    = self.worker.get_node("ns=5;i=136").get_value()
                self.machinefeedback["core_energy"] = core_energy
                # IQ VP
                iqvp                    = self.worker.get_node("ns=5;i=116").get_value()
                self.machinefeedback["iqvp"] = iqvp
                # IQ Holding Pressure
                iqhp                    = self.worker.get_node("ns=5;i=117").get_value()
                self.machinefeedback["iqhp"] = iqhp

                self.processactivate =False

                # TYPE SAVE TO DB CODE HERE !!!!!!!!!!!!

                    # DBPLAN save MachineID updatetime status(dumps(dict)) feedback(dumps(dict)) curve((dumps(dict))) ....


                #Clean act injection pressure&speed act motor power curve 
                self.actpressurecurve=[]
                self.actspeedcurve=[]
                self.motorpower=[]
                self.heaterpower=[]
                self.screwposition =[]
                self.timeindex =[]
        #Get current time
        current_time        = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.red.set(f'{self.machineid}_updatetiem',current_time)
        self.red.set(f'{self.machineid}_status',json.dumps(self.machinestatus))
        self.red.set(f'{self.machineid}_feedback',json.dumps(self.machinefeedback))
        self.red.set(f'{self.machineid}_curve',json.dumps(self.machinecurve))
if __name__ == "__main__":
    machineaddress = '192.168.1.15:4840'
    user = os.environ.get('user', 'localuser1622689641636')
    password= os.environ.get('password', '12345')
    Engel=engelagent(machineaddress,user,password,'Engel')
    Engel.connect()
    while True:
      Engel.collectdata()




