# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:41:50 2023

@author: cax
"""
# Act Volume : self.machinestatus["injection_pos"]["injection_volume1"] - self.machinefeedback["material_cushion"]
# Set Volume : self.machinestatus["injection_pos"]
def compare_ijpos_ijend (injection_postion,injection_end): #比較射出終點跟射出位置設定
    
    setting_injection_volume=float(injection_postion[0])-float(injection_postion[-1])#計算設定劑量
    real_injection_volume=float(injection_postion[0])-float(injection_end) #計算實際打入的劑量
    compare=real_injection_volume/setting_injection_volume #(實際劑量-設定劑量)/設定劑量
    # print(compare)
    if compare <=0.9:
        return [0,compare]
    elif compare<=1.1:
        return [1,compare]
    elif compare<1.3:
        return [2,compare]
    else:
        return [3,compare]

def injection_end_cau(injection_postion,injection_end):#比較殘餘劑量與射出劑量
    setting_injection_volume=injection_postion[0]-injection_postion[-1]#計算設定劑量
    compare=injection_end/setting_injection_volume
    if compare <0.2:
        return [0,compare]
    if compare >0.2 and compare<0.5:
        return [1,compare]
    else:
        return [2,compare]

def max_injection_pressure_compare_injection_pressure_setting(injection_pressure_set,max_injection_pressure): #比對實際最大射壓跟射壓設定值
    compare=float(max_injection_pressure)/float(injection_pressure_set)
    if compare>0.8:
        return [0,compare]
    elif compare>0.6:
        return [1,compare]
    else:
        return [2,compare]

def compare_flt_limit(fillingtime,fillingtimelimt):#比較充填時間與充填限制時間
    compare=float(fillingtimelimt)-float(fillingtime)
    if compare<1:
        return [0,compare]
    else:
        return [1,compare]

def compare_injectiondose_fltlimit(injection_postion_setting,fillingtimelimt):#比較射出行程和射出轉保時間
    ijdose=float(injection_postion_setting[0])-float(injection_postion_setting[-1])#計算設定劑量
    compare=ijdose/float(fillingtimelimt)
    # print(compare)
    if compare<3:
        return [0,compare]
    elif compare< 12:
        return [1,compare]
    else:
        return [2,compare]
    
def compare_max_ijspeed_postion(ijspeedsetting,injection_postion):#比較最高射速跟最高射速行程
    #將射速用max-min標準化，目的是為了去判斷整體射速設置，哪些射速是屬於低射速群哪些是高射速群，我比較的重點並不是我用最高射速射多少劑量，假設有人的射速設置[10,50,55,50,10]
    #射出位置為[20,18,15,13,10,8]這樣我可以說他只用最高射速射了(15-13)?計算出來的高射速占比應該不算準確，因為從整體射速配置來看 50 55 50這三這的射速配置應該算是高射速群集的
    #所以應該是要理解成我用高射速群集射了(18-10)才是公正的判斷方式
    ijspeedsetting=list(map(float,ijspeedsetting))
    # print('ijspeedsetting',ijspeedsetting)
    injection_postion=list(map(float,injection_postion))
    max_injectionspset=max(ijspeedsetting)
    min_injectionspset=min(ijspeedsetting)
    #如果只使用一段射速就沒有高速行程佔比的問題
    if max_injectionspset== min_injectionspset:
        return [3,100]
    standardization_speed_set=[]
    for i in ijspeedsetting:
        st=(i-min_injectionspset)/(max_injectionspset-min_injectionspset)
        standardization_speed_set.append(st)
    # print(ijspeedsetting)
    # print(standardization_speed_set)
    #接下來將射出位置轉為劑量百分比
    transform_postion_to_dose=[]
    totaldose=injection_postion[0]-injection_postion[-1]
    for i in range(4):
        dose=injection_postion[i]-injection_postion[i+1]
        percentage_of_dose=dose/totaldose
        transform_postion_to_dose.append(percentage_of_dose)
    # print(transform_postion_to_dose)
    #再來就是確認高射速群集佔多少比例的劑量，暫時將>0.7的當作高射速佔比
    pre=0
    for i in range(len(standardization_speed_set)):
        if standardization_speed_set[i] >0.7:
            pre=pre+transform_postion_to_dose[i]
    # print(pre)
    if pre< 0.25:
        return [0,pre]
    elif pre<0.5:
        return [1,pre]
    elif pre<0.75:
        return [2,pre]
    else :
        return [3,pre]

def settingspeed_vs_machinelimit(ijspeedsetting,machinelimit):#比較射速設定值VS機台上限
    ijspeedsetting=list(map(float, ijspeedsetting))
    maxijspeedset=max(ijspeedsetting)
    percentage_of_limit=maxijspeedset/machinelimit
    if percentage_of_limit<0.5:
        return [0,percentage_of_limit]
    elif percentage_of_limit <0.85:
        return [1,percentage_of_limit]
    else:
        return [2,percentage_of_limit]

def settingpressure_vs_machinelimit(ijpressuresetting,machinelimit):#比較射壓設定值vs機台上限
    percentage_of_limit=float(ijpressuresetting)/machinelimit
    if percentage_of_limit<0.5:
        return [0,percentage_of_limit]
    elif percentage_of_limit <0.85:
        return [1,percentage_of_limit]
    else:
        return [2,percentage_of_limit]
def settingmoldtemp_vs_moldtempsuggestion(moldtemp,suggestion) : #比較模溫設定值VS建議值
    suggestionlow=suggestion[0]
    suggestionhigh=suggestion[1]
    
    if float(moldtemp)<suggestionlow:
        return 0
    elif float(moldtemp)>suggestionhigh:
        return 1
    elif float(moldtemp)>=suggestionlow and float(moldtemp)<=suggestionhigh:
        ninetity=(suggestionhigh-suggestionlow)*0.9 +suggestionlow
        if float(moldtemp)<ninetity:
            return 2
        else:
            return 3

def settingmaterialtmp_vs_materialtmpsuggestion(settemp,suggestion) : #比較料管溫度設定值VS建議值
    settemp=settemp[1:].split(',')   
    suggestionlow=suggestion[0]
    suggestionhigh=suggestion[1]
    if float(settemp[0])<suggestionlow:
        return 0
    elif float(settemp[0])>suggestionhigh:
        return 1
    elif float(settemp[0])>=suggestionlow and float(settemp[0])<=suggestionhigh:
        ninetity=(suggestionhigh-suggestionlow)*0.9 +suggestionlow
        if float(settemp[0])<ninetity:
            return 2
        else:
            return 3
def check_store_postion(injectionpostion,storepostion):#檢查儲料位置是否合適
    injectionp=injectionpostion[0]
    if injectionp==storepostion:
        return 0
    elif storepostion<injectionp:
        return 1
    else:
        return 2
    
def check_backpressure(backpressuresetting,suggestion):#檢查背壓設定值與建議值
    backpressuresetting=backpressuresetting[1:].split(',')[0]
    suggestionlow=suggestion[0]
    suggestionhigh=suggestion[1]
    if float(backpressuresetting)<suggestionlow:
        return 0
    elif float(backpressuresetting)>suggestionhigh:
        return 1
    else:
        return 2
    
def compare_realinjection_ijspeedset(realspeed,speedset):#檢查實際設速vs設定值
    realspeedstr=realspeed.split(',')
    realspeedstr=realspeedstr[1:-1]
    realspeedlist=[]
    for i in realspeedstr:
        realspeedlist.append(float(i))
    speedset=list(map(float,speedset))
    speedsethigh=max(speedset)
    realspeedmax=max(realspeedlist)
    compare=realspeedmax/speedsethigh
    if compare<0.65:
        return [0,compare]
    elif compare<=1:
        return [1,compare]
    else:
        return [2,compare]
        
    
    
    