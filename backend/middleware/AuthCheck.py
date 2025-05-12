from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import create_engine, Column, Integer, String,DateTime,text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.responses import JSONResponse
db_url = "postgresql://postgres:postgres@Injection-Machine-Database:5432/cax"
engine = create_engine(db_url)

whitelist = ["/smc/injectionmachinemes/healthcheck", "/smc/injectionmachinemes/realtimedata","/smc/injectionmachinemes/user/login"]
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        #  CORS 預檢請求不驗證 Token
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if any(request.url.path.startswith(prefix) for prefix in whitelist):
            return await call_next(request)
        
        token = request.headers.get("accesstoken")
        returnData = {"status":"error","Message":""}
        if not token:
            print("[DEBUG] Middle Ware Reject Request (No accesstoken)")
            returnData["Message"] = "Token is required"
            print("[DEBUG] Create Error Message")
            return JSONResponse(
                status_code=403,
                content=returnData,
            )
        sql=f'''
            select count(*) as count from "UserConfig" where token  = '{token}'
        '''
        tokenactivate = "reject"
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                if int(row[0]) == 1:
                    tokenactivate = "approve"
        if tokenactivate == "reject":
            returnData["Message"] = "Permission denied"

            return JSONResponse(
                status_code=403,
                content=returnData,
            )



        return await call_next(request)