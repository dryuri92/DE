from .postgre import *
from .pand import *
from .query import *
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Dict
from abc import abstractmethod, ABC
import asyncpg
import asyncio

class Engine(ABC):
    def __init__(self, **kwargs):
        raise NotImplementedError("It is abstract class. Need to implementation")
    @abstractmethod
    def connect(self)->bool:
        ...
    @abstractmethod
    async def fetch(self,query:Query, parameters: list[any], **kwargs):
        ...
    @abstractmethod
    async def execute(self,query:Query, parameters: list[any], **kwargs):
        ...
    
class PandasEngine(Engine):
    def __init__(self, **kwargs):
        self._filename = kwargs["tablename"]
        self._df = pd.DataFrame()
    def connect(self)->bool:
        return True
    async def fetch(self,query:Query, parameters: list[any], **kwargs):
        try:
            self._df = pd.read_csv(self._filename, index_col=False)
            params = []
            print(f"2.DEBUG PARAMETERS {parameters} with {query.dateField} with {query.dateType}")
            for p in parameters:
                if (type(p) is datetime):
                    s = p.strftime("%Y-%m-%dT%H:%M:%S")
                    params.append(f'"{s}"')
                elif (type(p) is str):
                    params.append(f"'{p}'")
                else:
                    params.append(p)
            q_ = query.query['filter'].format(*tuple(params))
            self._df[query.dateField] = self._df[query.dateField].values.astype(query.dateType)
            print(f"it is query{self._df} and {q_}")    
            df=self._df.query(query.query['filter'].format(*tuple(params)))
            print(f"it is query{df} and 1")
            df=df.groupby(query.query['group']).apply(lambda x:x)
            print(f"it is query{df} and 2")
            df = df.filter(items=query.query["fields"])
            print(f"it is query{df} and 3")
        except Exception as E:
            print(f"Meet except {E}")
            raise RuntimeError(f"Meet except {E}")
        print(f"2.debug it is query{df} and {query.query['group']}")
        print([df.iloc[i].to_dict() for i in range(len(df))])
        await asyncio.sleep(0)
        return [df.iloc[i].to_dict() for i in range(len(df))]
    async def execute(self,query:Query, parameters: list[any], **kwargs):
        try:
            self._df = self._df._append(query.query,ignore_index=True)
            self._df.to_csv(self._filename, index=False)
        except Exception as E:
            raise RuntimeError(f"Can not write data to file: {E}")
        await asyncio.sleep(0)

class PostgreEngine(Engine):
    def __init__(self, **kwargs):
        self._connected = False
        self._conn=None
        print(f"postgre kwargs is {kwargs}")
        try:
            self._host = kwargs["dbhost"]
            self._user = kwargs["dbuser"]
            self._password = kwargs["dbpassword"]
            self._dbname = kwargs["dbname"]
            self._tablename = kwargs["tablename"]
        except KeyError as K:
            print(f"Not enough argument to Postgre connection {K}")
    async def establishConnection(self):
        try:
            self._conn = await asyncpg.connect(user=self._user,
                                               password=self._password,
                                               database=self._dbname,
                                               host=self._host)
            self._connected=True
        except:
            print("Could not establish connection")
    def connect(self)->bool:
        return self._connected
    async def fetch(self,query:Query, parameters: list[any], **kwargs):
        print(f"DEBUG [fetch] {parameters} {query.query}")
        try:
            values = await self._conn.fetch(
            query.query,
            *parameters,
            )
        except Exception as E:
            print(f"fetch exception is {E}")
            raise RuntimeError("fetch exception is {E}")
        print(f"Return {values}")
        return values
    async def execute(self,query:Query, parameters: list[any], **kwargs):
        print(parameters)
        async with self._conn.transaction():
            cmd = f"{query.query} {tuple(parameters)};"
            print("cmd is ", cmd)
            try:
                await self._conn.execute(f"{query.query} {tuple(parameters)};")
            except Exception as E:
                print(f"Exceptionis {E}")
                raise RuntimeError(f"Can not execute a query: {E}")
    
def GetDbEngine(config: dict)->Engine:
    engine = config["engine"]
    print(f"confing {config}")
    if engine == "pandas":
        return PandasEngine(**config)
    elif (engine == "postgres"):
        return PostgreEngine(**config)
    
class QueryBuilder:
    def __new__(cls, engine: str, action: str, **kwargs):
        parameters=[]
        if (engine=="postgres"):
            fields = kwargs.get("fields") if kwargs.get("fields") else []
            print(f"DEBUG in query builder {cls} 1")
            query = PGSQLQuery(
                fields=fields,
                tablename=kwargs["tablename"],
                action=action)
            print(f"DEBUG in query builder {cls} 2")
            if (action == "insert"):
                parameters.extend(fields)
            print(f"DEBUG in query builder {kwargs} 3")
            if ("filters" in kwargs):
                for compare, filters in kwargs["filters"].items():

                    query.filter(filters=[f["attribute"] for f in filters  if (f["value"] is not None)], compare=compare)
                    parameters.extend([f["value"] for f in filters  if (f["value"] is not None)])
            print(f"DEBUG in query builder {cls} 4")
            if ("groupBy" in kwargs):
                query.groupBy(kwargs["groupBy"])
            print(f"DEBUG in query builder {cls} 5")
            if ("granularity" in kwargs):
                query.granularity(kwargs["dateField"],kwargs["granularity"])
            print(f"DEBUG in query builder {cls} 6")
            if ("values" in kwargs):
                items = kwargs["values"].items()
                parameters = [item[1] for item in items]
                query.values([item[0] for item in items])
            print(f"DEBUG in query builder {cls} 7")
            return query, parameters
        elif (engine == "pandas"):
            fields = kwargs.get("fields") if kwargs.get("fields") else []
            query = PandasQuery(fields=fields, tablename="events.csv", action=action)
            if (action == "insert"):
                parameters.extend(fields)
            if ("filters" in kwargs):
                print("debug 1")
                for compare, filters in kwargs["filters"].items():
                    print(f"debug 1: filters is {filters}")
                    query.filter(filters=[f["attribute"] for f in filters if (f["value"] is not None)], compare=compare)
                    parameters.extend([f["value"] for f in filters if (f["value"] is not None)])
            if ("groupBy" in kwargs):
                query.groupBy(kwargs["groupBy"])
            if ("granularity" in kwargs):
                print("debug 2", kwargs["dateField"], kwargs["granularity"])
                query.granularity(kwargs["dateField"],kwargs["granularity"])
            if ("values" in kwargs):
                query.values(kwargs["values"])
            print("debug 3")
            return query, parameters
        return None, None

    

    

