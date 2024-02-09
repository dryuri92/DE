from datetime import datetime
import pytest
from db.postgre import PGSQLQuery

@pytest.fixture
def pgsql_query():
    return PGSQLQuery(tablename="test_table", fields=["field1", "field2"])

def test_select_query(pgsql_query):
    expected_query = 'SELECT "field1","field2" FROM test_table'
    assert pgsql_query.query == expected_query

def test_values(pgsql_query):
    values = ["value1", "value2"]
    pgsql_query.values(values)
    assert pgsql_query._values == "(\"value1\",\"value2\")"