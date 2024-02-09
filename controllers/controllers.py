from db import QueryBuilder, Query, Engine, GetDbEngine
import asyncio
from datetime import datetime
from models import Event, Filters, Granularity, Filter

class Controller:
    #
    def __init__(self, config: dict):
        self._config = config
        self._engine = GetDbEngine(self._config)
        print(f"meet the engine:{self._engine}")
    #
    async def connect(self):
        if not self._engine.connect():
            await self._engine.establishConnection()
    async def getEvents(self,
                        metrics: str,
                        group: str,
                        granularity: Granularity,
                        *,
                        filters: list[str]|None = None,
                        start_date: datetime | None=None,
                        end_date: datetime | None=None,
                        )-> dict:
        
        print(f"DEBUG[controller]: filters, gran {filters} and {granularity.value}")
        query, parameters = QueryBuilder(
                              engine=self._config["engine"],
                              action="SELECT",
                              tablename = self._config["tablename"],
                              fields=metrics.split(","),
                              filters={
                                "=": filters,
                                ">": [{"attribute":self._config["datetimeField"], "value": start_date}],
                                "<": [{"attribute":self._config["datetimeField"], "value": end_date}]
                              },
                              granularity=granularity.value,
                              dateField = self._config["datetimeField"],
                              groupBy=group.split(","))
        try:
            print(f"meet the query {query.query} with parameters {parameters}")
            result = await self._engine.fetch(query, parameters)
        except:
             raise Exception("Can not execute Query")
        return result
    #
    async def postEvent(self,
                        event: Event)->bool:
        query, parameters = QueryBuilder(
                                engine=self._config["engine"],
                                action="INSERT",
                                tablename = self._config["tablename"],
                                values = {"id": event.id,
                                          "event_date": event.event_date.strftime("%Y-%m-%dT%H:%M:%S"),
                                          "attribute1": event.attribute1,
                                          "attribute2": event.attribute2,
                                          "attribute3": event.attribute3,
                                          "attribute4": event.attribute4,
                                          "attribute5": event.attribute5,
                                          "attribute6": event.attribute6,
                                          "metric1": event.metric1,
                                          "metric2": event.metric2})
        try:
            print(f"meet the query {query.query} with parameters {parameters}")
            await self._engine.execute(query, parameters)
        except:
            raise Exception("Can not execute Query")
        return True