from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String,DateTime,text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import json
import uuid
import bcrypt 
logging.basicConfig(
    level=logging.INFO,  # 可改為 DEBUG、WARNING、ERROR、CRITICAL
    format='%(levelname)s - %(asctime)s - %(message)s'
)


userrouter = APIRouter()

db_url = "postgresql://postgres:postgres@Injection-Machine-Database:5432/cax"
engine = create_engine(db_url)
Base = declarative_base()

Base = declarative_base()

class UserConfig(Base):
    __tablename__ = 'UserConfig'
    id            = Column(Integer,primary_key=True)
    created_at    = Column(DateTime(timezone = False), server_default=func.now())
    username      = Column(String)
    useraccount   = Column(String)
    userpassword  = Column(String)
    token         = Column(String)

class Usercreatebody(BaseModel):
    username:str
    useraccount:str
    userpassword:str

class Userloginbody(BaseModel):
    useraccount:str
    userpassword:str

@userrouter.post("/smc/injectionmachinemes/user/createuser")
async def insertdata(requestData:Usercreatebody):
    returnData       = {"status":"error"}
    username         = requestData.username
    useraccount      = requestData.useraccount
    userpassword     = requestData.userpassword
    
    try:
        hashed_password = bcrypt.hashpw(userpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usertoken = uuid.uuid4()
        insert_sql = UserConfig.__table__.insert().values(
                    username     = username,
                    useraccount  = useraccount,
                    userpassword = hashed_password,
                    token        = usertoken
                )
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(insert_sql)
        session.commit()
        session.close()
        returnData = {"status": "success"}
    except Exception as e:
        print(e)
        logging.error("Create user to db failed ...")
        pass
    return returnData

@userrouter.post("/smc/injectionmachinemes/user/login")
async def insertdata(requestData:Userloginbody):
    returnData       = {"status":"error"}
    useraccount      = requestData.useraccount
    userpassword     = requestData.userpassword
    
    try:
        sql=f'''
            select userpassword,token from "UserConfig" where useraccount  = '{useraccount}'
        '''
        dbpassword = ''
        usertoken  = ''
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            for row in result:
                dbpassword = row[0]
        if dbpassword == '':
            returnData = {"status": "error","Message":"Invaild account"}
        else:
            if bcrypt.checkpw(userpassword.encode('utf-8'), dbpassword.encode('utf-8')):
                usertoken = row[1]
                returnData = {"status": "success","Data":{"token":usertoken}}
            else:
                returnData = {"status": "error","Message":"Invaild password"}
    except Exception as e:
        print(e)
        logging.error("User login API Crashed ...")
        pass
    return returnData






