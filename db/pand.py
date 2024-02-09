from .query import Query
import pandas as pd

class PandasQuery(Query):
    def __init__(self, tablename, fields, action="SELECT"):
        super().__init__(tablename=tablename, fields=fields, action=action)
        self._dateField = None
        self._dttype = 'datetime64[h]'
        self._query=None
        self.numParameters = 0
        if (action == "SELECT"):
            self._select = fields
        elif (action == "INSERT"):
            ...
    def filter(self, filters: list[str], compare: str="="):
        if compare == "=":
            compare="=="
        if (len(filters) > 0):
            if (len(self._filter) > 0):
                self._filter = f"{self._filter} and "
            self._filter = self._filter + ' and '.join([f'({filtername}{compare}'+'{' + str(i+self.numParameters) + '})' for i, filtername in enumerate(filters)])
            self.numParameters += len(filters)
    def groupBy(self, groupping: list[str]):
        if (len(groupping) > 0):
            self._group = groupping
            self._select.extend(groupping)
    def granularity(self, dateField: str, granularity: str):
        if (granularity in ["hourly", "daily"]):
            if (granularity == "hourly"):
                self._select.append(dateField)
                self._dttype = 'datetime64[h]'
            elif (granularity == "daily"):
                self._select.append(dateField)
                self._dttype = 'datetime64[D]'
            self._dateField = dateField
    def values(self, values:list|dict):
        self._values = values
    @property
    def dateField(self):
        return self._dateField
    @property
    def dateType(self):
        return self._dttype
    @property
    def query(self):
        if (self._action == "SELECT"):
            self._query={"fields": self._select, "filter": self._filter, "group": self._group, "datetime":self._dttype}
        elif (self._action == "INSERT"):
            return self._values
        return self._query
