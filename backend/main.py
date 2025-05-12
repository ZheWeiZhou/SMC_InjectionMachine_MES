from fastapi import FastAPI
import uvicorn
from middleware.AuthCheck import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from routers.historyrouter import historyrouter
from routers.realtimedatarouter import realtimedatarouter
from routers.commandrouter import commandrouter
from routers.userrouter import userrouter
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

app.include_router(historyrouter)
app.include_router(realtimedatarouter)
app.include_router(commandrouter)
app.include_router(userrouter)

@app.get("/smc/injectionmachinemes/healthcheck")
async def healthcheck():

    returnData = {"status":"success"}
    return returnData

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)