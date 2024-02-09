import pytest
import pandas as pd
from db.pand import PandasQuery

@pytest.fixture
def pandas_query():
    return PandasQuery(tablename="test_table", fields=["field1", "field2"])

def test_filter(pandas_query):
    pandas_query.filter(["field1", "field2"])
    assert pandas_query._filter == "(field1=={0}) and (field2=={1})"
    assert pandas_query.numParameters == 2

def test_granularity_hourly(pandas_query):
    pandas_query.granularity("date_column", "hourly")
    assert pandas_query._select == ["field1", "field2", "date_column"]
    assert pandas_query._dttype == 'datetime64[h]'

def test_granularity_daily(pandas_query):
    pandas_query.granularity("date_column", "daily")
    assert pandas_query._select == ["field1", "field2", "date_column"]
    assert pandas_query._dttype == 'datetime64[D]'

def test_values(pandas_query):
    values = {"field1": 10, "field2": "value"}
    pandas_query.values(values)
    assert pandas_query._values == values

def test_dateType(pandas_query):
    assert pandas_query.dateType == 'datetime64[h]'

def test_query_insert(pandas_query):
    pandas_query._action = "INSERT"
    values = {"field1": 10, "field2": "value"}
    pandas_query.values(values)
    assert pandas_query.query == values

