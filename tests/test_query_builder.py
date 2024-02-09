import pytest
from db import QueryBuilder

def test_postgres_query_builder_insert():
    fields = ["field1", "field2"]
    values = {"field1": 10, "field2": "value"}
    query, parameters = QueryBuilder(engine="postgres", action="insert", tablename="test_table", fields=fields, values=values)
    assert parameters == [10, "value"]

def test_postgres_query_builder_with_filters():
    filters = {"=": [{"attribute": "field1", "value": 10}]}
    query, parameters = QueryBuilder(engine="postgres", action="select", tablename="test_table", filters=filters)
    assert parameters == [10]
