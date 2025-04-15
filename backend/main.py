from fastapi import FastAPI
import uvicorn
from routers.historyrouter import historyrouter

app = FastAPI()
app.include_router(historyrouter)

@app.get("/smc/injectionmachinemes/healthcheck")
async def healthcheck():

    returnData = {"status":"success"}
    return returnData

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)