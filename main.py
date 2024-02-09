from __future__ import annotations
import uvicorn
from datetime import datetime
from typing import  Optional, Annotated

from fastapi import FastAPI, Query, HTTPException, status, Depends, Request

from models import Event, Granularity, Filter
from controllers import Controller
import os

config = {}

try:
    config["engine"] = os.environ["ENGINE"].rstrip()
    config["dbname"] = os.environ["DBNAME"].rstrip()
    config["dbhost"] = os.environ["DBHOST"].rstrip()
    config["dbport"] = int(os.environ["DBPORT"].rstrip())
    config["dbuser"] = os.environ["DBUSER"].rstrip()
    config["dbpassword"] = os.environ["DBPASSWORD"].rstrip()
    config["tablename"] = os.environ["DBTABLE"].rstrip()
    config["datetimeField"] = os.environ["DBDATEFIELD"] or "event_date"
except Exception as E:
    print(f"Exception caught switch to pandas engine: {E}")
    config["engine"] = "pandas"
    config["tablename"] = "./data/events.csv"
    config["datetimeField"] = "event_date"
try:
    APP_HOST = os.environ["APP_HOST"]
    APP_PORT = int(os.environ["APP_PORT"])
except:
    APP_HOST = "127.0.0.1"
    APP_PORT =  8888

#DEFAULT POSTGRESQL CONFIG
#config = {"engine":"postgres",
#          "dbname": "test_db",
#          "dbhost": "localhost",
#          "dbport":5432,
#          "dbuser":"root",
#          "dbpassword":"root",
#          "tablename": "cd.events",
#          "datetimeField":"event_date"}

app = FastAPI(
    title='Senior DE',
    controller = Controller(config),
    version='1.0.1',
)

def requestController(app_name: str):
    """Get a decorator represented a controller to connect to database
    Args:
        app_name: str
            Name of controller
    """
    async def inner(request: Request):
        requested = request.app.extra[f'{app_name}']
        await requested.connect()
        return requested
    return inner

@app.get('/analytics/query')
async def get_analytics_data(
    metrics: str,
    group_by: str = Query(..., alias='groupBy'),
    filters: Annotated[list[str], Query(..., alias='filters')]=None,
    granularity: Granularity = Query(..., alias='granularity'),
    start_date: Optional[datetime] = Query(None, alias='startDate'),
    end_date: Optional[datetime] = Query(None, alias='endDate'),
    controller = Depends(requestController("controller"))
):
    """
    Get analytics data for events
    """
    try:
        response = await controller.getEvents(
                                        metrics,
                                        group_by,
                                        granularity,
                                        filters=[Filter.parser(f) for f in filters],
                                        start_date=start_date,
                                        end_date=end_date)
        return response
    except Exception as E:
        raise HTTPException(status_code=405, detail=f"Bad request{E}") 

@app.post('/event')
async def add_event(body: Event,
              controller = Depends(requestController("controller"))):
    """
    Add an event
    """
    try:
        await controller.postEvent(body)
    except Exception as E:
        raise HTTPException(status_code=405, detail=f"Bad request{E}") 
    return status.HTTP_200_OK

if __name__ == "__main__":
    uvicorn.run("main:app", host=f"{APP_HOST}", port=APP_PORT)
