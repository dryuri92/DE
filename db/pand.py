from .query import Query
import pandas as pd

class PandasQuery(Query):
    """A class that extends the base Query class and adds functionality specific to working with Pandas DataFrames."""
    def __init__(self, tablename, fields, action="SELECT"):
        """Initializes a new instance of the PandasQuery class.
        
        Args:
            tablename (str): The name of the table or dataset.
            fields (list): A list of field names to include in the query.
            action (str, optional): The action to perform (e.g., SELECT, INSERT). Defaults to "SELECT".
        """
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
        """Filters the query results based on a set of conditions.
        
        Args:
            filters (list[str]): A list of filter expressions (e.g., "field_name operator value").
            compare (str, optional): The comparison operator to use (e.g., =, !=, >, <). Defaults to "=".
        """
        if compare == "=":
            compare="=="
        if (len(filters) > 0):
            if (len(self._filter) > 0):
                self._filter = f"{self._filter} and "
            self._filter = self._filter + ' and '.join([f'({filtername}{compare}'+'{' + str(i+self.numParameters) + '})' for i, filtername in enumerate(filters)])
            self.numParameters += len(filters)
    def groupBy(self, groupping: list[str]):
        """Groups the query results by one or more columns.
        
        Args:
            groupping (list[str]): A list of column names to group by.
        """
        if (len(groupping) > 0):
            self._group = groupping
            self._select.extend(groupping)
    def granularity(self, dateField: str, granularity: str):
        """Sets the time granularity for aggregation operations.
        
        Args:
            dateField (str): The name of the date/time column.
            granularity (str): The desired level of granularity (e.g., hourly, daily).
        """
        if (granularity in ["hourly", "daily"]):
            if (granularity == "hourly"):
                self._select.append(dateField)
                self._dttype = 'datetime64[h]'
            elif (granularity == "daily"):
                self._select.append(dateField)
                self._dttype = 'datetime64[D]'
            self._dateField = dateField
    def values(self, values:list|dict):
        """Sets the values to be inserted into the target table.
        
        Args:
            values (list | dict): A list or dictionary of values.
        """
        self._values: list | dict = values
        self._values = values
    @property
    def dateField(self) -> str:
        """Returns the name of the date/time column."""
        return self._dateField
    @property
    def dateType(self) -> str | None:
        """Returns the time granularity of the query."""
        return self._dttype
    @property
    def query(self) -> str | None:
        """Gets the final query"""
        if (self._action == "SELECT"):
            self._query={"fields": self._select, "filter": self._filter, "group": self._group, "datetime":self._dttype}
        elif (self._action == "INSERT"):
            return self._values
        return self._query
