from abc import abstractmethod, ABC

class Query(ABC):
    def __init__(self,tablename, fields, action):
        self.__tablename__ = tablename
        self._values=""
        self._select=""
        self._modify=""
        self._filter=""
        self._group=""
        self._action=action
        self._query=""
        self.numParameters = 0
    @abstractmethod
    def filter(self, filters: list[str], compare: str="="):
        ...
    @abstractmethod
    def groupBy(self, filters: list[str], compare: str="="):
        ...
    @abstractmethod
    def granularity(self, filters: list[str], compare: str="="):
        ...
    @abstractmethod
    def values(self, filters: list[str], compare: str="="):
        ...