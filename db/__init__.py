from .postgre import *
from .pand import *
from .query import *
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
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
    """Pandas-based implementation of the Engine interface."""
    def __init__(self, **kwargs):
        """Initializes the PandasEngine instance.
        
        Args:
            filename (str): Path to the CSV file.
        """
        self._filename = kwargs["tablename"]
        self._df = pd.DataFrame()
    def connect(self)->bool:
        """Connects to the underlying storage system - always successful in this case.
        
        Returns:
            bool: Always returns True.
        """
        return True
    async def fetch(self,query:Query, parameters: list[any], **kwargs) -> List[Dict[str, Any]]:
        """Fetches records matching the given query and parameters.
        
        Args:
            query (Query): The query object specifying the selection criteria.
            parameters (List[Any]): Parameters needed to evaluate the query.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched records.
        """
        try:
            self._df = pd.read_csv(self._filename, index_col=False)
            params = []
            for p in parameters:
                if (type(p) is datetime):
                    s = p.strftime("%Y-%m-%dT%H:%M:%S")
                    params.append(f'"{s}"')
                elif (type(p) is str):
                    params.append(f"'{p}'")
                else:
                    params.append(p)
            self._df[query.dateField] = self._df[query.dateField].values.astype(query.dateType)
            df=self._df.query(query.query['filter'].format(*tuple(params)))
            df=df.groupby(query.query['group']).apply(lambda x:x)
            df = df.filter(items=query.query["fields"])
        except Exception as E:
            raise RuntimeError(f"Meet except {E}")
        await asyncio.sleep(0)
        return [df.iloc[i].to_dict() for i in range(len(df))]
    async def execute(self,query:Query, parameters: list[any], **kwargs):
        """Executes the given query against the underlying storage system.
        
        Args:
            query (Query): The query object specifying the execution details.
            parameters (List[Any]): Parameters needed to execute the query.

        """
        try:
            self._df = self._df._append(query.query,ignore_index=True)
            self._df.to_csv(self._filename, index=False)
        except Exception as E:
            raise RuntimeError(f"Can not write data to file: {E}")
        await asyncio.sleep(0)

class PostgreEngine(Engine):
    """PostgreSQL-based implementation of the Engine interface."""
    def __init__(self, **kwargs):
        """Initializes the PostgreEngine instance.

        Raises:
            KeyError: When mandatory initialization parameters are missing.

        Args:
            dbhost (str): Database host address.
            dbuser (str): Username to access the database.
            dbpassword (str): Password to authenticate the user.
            dbname (str): Name of the database to interact with.
            tablename (str): Table name within the database.
        """
        self._connected = False
        self._conn=None
        try:
            self._host = kwargs["dbhost"]
            self._user = kwargs["dbuser"]
            self._password = kwargs["dbpassword"]
            self._dbname = kwargs["dbname"]
            self._tablename = kwargs["tablename"]
        except KeyError as K:
            print(f"Not enough argument to Postgre connection {K}")
    async def establishConnection(self):
        """Establishes an asynchronous connection to the PostgreSQL server."""
        try:
            self._conn = await asyncpg.connect(user=self._user,
                                               password=self._password,
                                               database=self._dbname,
                                               host=self._host)
            self._connected=True
        except:
            print("Could not establish connection")
    def connect(self)->bool:
        """Checks if connected to the PostgreSQL server."""
        return self._connected
    async def fetch(self,query:Query, parameters: List[any], **kwargs)-> List[Dict[str, Any]]:
        """Queries the PostgreSQL server and returns the result.

        Args:
            query (Query): The query object specifying the selection criteria.
            parameters (List[any]): Parameters needed to evaluate the query.

        Returns:
            List[Dict[str, any]]: Results returned from the executed query.

        Raises:
            RuntimeError: In case of an unexpected exception during fetch.
        """
        try:
            values = await self._conn.fetch(
            query.query,
            *parameters,
            )
        except Exception as E:
            raise RuntimeError("fetch exception is {E}")
        return values
    async def execute(self,query:Query, parameters: List[any], **kwargs):
        """Executes the given query on PostgreSQL server.
        
        Args:
            query (Query): The query object specifying the execution details.
            parameters (List[Any]): Parameters needed to execute the query.

        """
        async with self._conn.transaction():
            try:
                await self._conn.execute(f"{query.query} {tuple(parameters)};")
            except Exception as E:
                raise RuntimeError(f"Can not execute a query: {E}")
    
def GetDbEngine(config: dict)->Engine:
    """Retrieves data source"""
    engine = config["engine"]
    print(f"confing {config}")
    if engine == "pandas":
        return PandasEngine(**config)
    elif (engine == "postgres"):
        return PostgreEngine(**config)
    
class QueryBuilder:
    def __new__(cls, engine: str, action: str, **kwargs):
        """Builds a query object based on the given parameters.

        Args:
            engine (str): Database engine identifier. Can be either "postgres" or "pandas".
            action (str): Type of query. Can be either "select" or "insert".
            **kwargs: Additional keyword arguments depending on the chosen engine.

        Returns:
            Optional[Tuple]: A tuple containing the built query object and a list of parameters.
        """
        parameters=[]
        if (engine=="postgres"):
            fields = kwargs.get("fields") if kwargs.get("fields") else []
            query = PGSQLQuery(
                fields=fields,
                tablename=kwargs["tablename"],
                action=action)
            if (action == "insert"):
                parameters.extend(fields)
            if ("filters" in kwargs):
                for compare, filters in kwargs["filters"].items():

                    query.filter(filters=[f["attribute"] for f in filters  if (f["value"] is not None)], compare=compare)
                    parameters.extend([f["value"] for f in filters  if (f["value"] is not None)])
            if ("groupBy" in kwargs):
                query.groupBy(kwargs["groupBy"])
            if ("granularity" in kwargs):
                query.granularity(kwargs["dateField"],kwargs["granularity"])
            if ("values" in kwargs):
                items = kwargs["values"].items()
                parameters = [item[1] for item in items]
                query.values([item[0] for item in items])
            return query, parameters
        elif (engine == "pandas"):
            fields = kwargs.get("fields") if kwargs.get("fields") else []
            query = PandasQuery(fields=fields, tablename=kwargs["tablename"], action=action)
            if (action == "insert"):
                parameters.extend(fields)
            if ("filters" in kwargs):
                for compare, filters in kwargs["filters"].items():
                    query.filter(filters=[f["attribute"] for f in filters if (f["value"] is not None)], compare=compare)
                    parameters.extend([f["value"] for f in filters if (f["value"] is not None)])
            if ("groupBy" in kwargs):
                query.groupBy(kwargs["groupBy"])
            if ("granularity" in kwargs):
                query.granularity(kwargs["dateField"],kwargs["granularity"])
            if ("values" in kwargs):
                query.values(kwargs["values"])
            return query, parameters
        return None, None

    

    

