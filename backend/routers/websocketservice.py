from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime
import json
import sys
import os
from controler.powermeter_handler import PowerMeterCollecter
from controler.machine_endsignal_handler import MachineEndSignalHandler


WebSocketService= APIRouter()


@WebSocketService.websocket("/ws/realtimedata/power/current/{machine_id}/{interval_ms}")
async def stream_machine_current(websocket: WebSocket, machine_id: str, interval_ms:int):
    client_host= websocket.client.host
    await websocket.accept()
    min_interval= 0.1
    polling_interval= max(interval_ms / 1000, min_interval)
    PowerMeter= PowerMeterCollecter()
    try: 
       while True:
           powerresponse= PowerMeter.getcurrent(machine_id)
           
           data= {
               "machine_id": machine_id,
               "current_a":  powerresponse["current_a"],
               "current_b":  powerresponse["current_b"],
               "current_c":  powerresponse["current_c"],
               "online":  powerresponse["online"],
           }
           await websocket.send_json(data)
           await asyncio.sleep(polling_interval)
    except WebSocketDisconnect:
        print(f"{client_host} disconnet {machine_id} current websocket")

@WebSocketService.websocket("/ws/realtimedata/power/currentcurve/{machine_id}")
async def stream_machine_current(websocket: WebSocket, machine_id: str):
    client_host= websocket.client.host
    await websocket.accept()
    PowerMeter= PowerMeterCollecter()
    lastupdatetime = ''
    try: 
       while True:
           powerresponse= PowerMeter.getcurrentcurve(machine_id)
           if powerresponse["updatetime"] !=-1 and powerresponse["updatetime"] != lastupdatetime:
               lastupdatetime = powerresponse["updatetime"]
               data= {
                    "machine_id": machine_id,
                    "current_a":  powerresponse["current_a"],
                    "current_b":  powerresponse["current_b"],
                    "current_c":  powerresponse["current_c"],
                    "updatetime":powerresponse["updatetime"]
                }
               await websocket.send_json(data)
           await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"{client_host} disconnet {machine_id} current websocket")

@WebSocketService.websocket("/ws/realtimedata/machine/cycleEndSignal/{machine_id}")
async def stream_machine_current(websocket: WebSocket, machine_id: str):
    client_host= websocket.client.host
    await websocket.accept()
    lastupdatetime = -1
    supportmachinelist = ["TOYO","Engel-120"]
    if machine_id not in supportmachinelist:
        await websocket.send_json({"error":"Invalid Machine ID"})
        await websocket.close()
        return
    try: 
       while True:
           updatetime= MachineEndSignalHandler.getfeedbackupdatetime(machine_id)
           if lastupdatetime !=-1 and updatetime != lastupdatetime:
               lastupdatetime = updatetime
               data= {
                    "machine_id": machine_id,
                }
               await websocket.send_json(data)
           lastupdatetime = updatetime
           await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"{client_host} disconnet {machine_id} cycleEndSignal websocket")
           
