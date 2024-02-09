from datetime import datetime
from .query import Query

class PGSQLQuery(Query):
    def __init__(self, tablename, fields, action="SELECT"):
        super().__init__(tablename=tablename, fields=fields, action=action)
        self._query=f"{action} " + "{body}" + "{condition1}" + "{condition2}"
        self.numParameters = 0
        if (action == "SELECT"):
            self._query = f"{action} " + "{body}" + f" FROM {self.__tablename__}" + "{condition1}" + "{condition2}"
            self._select = ",".join([f'"{f}"' for i, f in enumerate(fields)])
            if (len(fields)==0):
                self._select = "*"
        elif (action == "INSERT"):
            self._query = f"{action} INTO "+ f"{self.__tablename__}" + " {body} " + " VALUES "
    def filter(self, filters: list[str], compare: str="="):
        if (len(filters) > 0):
            print(self._filter)
            if self._filter.find("WHERE") < 0:
                self._filter = f"{self._filter} WHERE "
                print("after", self._filter)
            else:
                self._filter = f"{self._filter} AND "
            self._filter = self._filter + " AND ".join([f'("{filtername}"{compare}${i+1+self.numParameters})' for i, filtername in enumerate(filters)])
            #self.query = f"{self.query} {conditions}"
            self.numParameters += len(filters)
    def groupBy(self, groupping: list[str]):
        if (len(groupping) > 0):
            self._group = " GROUP BY " + ",".join(([f'"{f}"' for  f in groupping])) + ","+ self._select
            self._select = f'{self._select},' + ",".join(([f'"{f}"' for  f in groupping]))
    def granularity(self, dateField: str, granularity: str):
        if (granularity in ["hourly", "daily"]):
            if (granularity == "hourly"):
                self._select = f"""{self._select},date_trunc('hour', "{dateField}") AS {dateField}"""
                self._group = f'{self._group},"{dateField}"'
            elif (granularity == "daily"):
                self._select = f"""{self._select},date_trunc('day', "{dateField}")  AS {dateField}"""
                self._group = f'{self._group},"{dateField}"'
    def values(self, values:list[str]):
        self._values = "(" + ",".join([f'"{v}"' for v in values]) + ")"
    @property
    def query(self):
        if (self._action == "SELECT"):
            self._query=self._query.format(body=self._select, condition1=self._filter, condition2=self._group)
        elif (self._action == "INSERT"):
            self._query=self._query.format(body=self._values)
        return self._query