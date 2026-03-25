from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime
import json
import sys
import os
from controler.powermeter_handler import PowerMeterCollecter


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

           
