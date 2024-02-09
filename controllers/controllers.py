from db import QueryBuilder, GetDbEngine
from datetime import datetime
from models import Event, Granularity

class Controller:
    #
    def __init__(self, config: dict):
        """Initialize a controller instance.

        Args:
            config: Configuration settings."""
        self._config = config
        self._engine = GetDbEngine(self._config)
        print(f"meet the engine:{self._engine}")
    #
    async def connect(self):
        """Connect to the configured database. """
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
        """Fetch events from the database according to the provided configurations.
            Args:
                metrics: Comma-separated list of metric keys.
                group: Group key(s), separated by commas.
                granularity: Granularity enum indicating the resolution of data points.
                filters: Optional list of equal comparisons to apply.
                start_date: Start date for time series filter.
                end_date: End date for time series filter.
            Returns:
                Dictionary containing requested metrics organized by groups.
        """
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
            result = await self._engine.fetch(query, parameters)
        except:
             raise Exception("Can not execute Query")
        return result
    #
    async def postEvent(self,
                        event: Event)->bool:
        """Insert a single event entry into the database.
            Args:
                event: An instance of the Event model.
            Returns:
                 Boolean indicating success status.
        """
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
            await self._engine.execute(query, parameters)
        except:
            raise Exception("Can not execute Query")
        return True