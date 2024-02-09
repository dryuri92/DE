#!/bin/sh
# GET-1
echo "get-1"
curl -X 'GET' \
  'http://localhost:8888/analytics/query?metrics=metric1%2Cmetric2&groupBy=attribute1%2Cattribute2&filters=attribute%3Aattribute3%2Cvalue%3A1&filters=attribute%3Aattribute4%2Cvalue%3Atest&granularity=hourly&startDate=2012-07-03T08%3A00%3A00&endDate=2012-07-03T11%3A21%3A00' \
  -H 'accept: application/json'
# POST-1
echo "\n post-1"
curl -X 'POST' \
  'http://localhost:8888/event' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 101,
  "event_date": "2011-07-03T08:05:08",
  "attribute1": 198,
  "attribute2": 3,
  "attribute3": 4,
  "attribute4": "test-post",
  "attribute5": "12345",
  "attribute6": false,
  "metric1": 12,
  "metric2": 5.5
}'
# GET-2
echo "\n get-2"
curl -X 'GET' \
  'http://localhost:8888/analytics/query?metrics=metric1&groupBy=attribute5%2Cattribute6&filters=attribute%3Aattribute6%2Cvalue%3Atrue&granularity=daily&startDate=2011-07-03T08%3A00%3A00' \
  -H 'accept: application/json'
# POST-2
echo "\n post-2"
curl -X 'POST' \
  'http://localhost:8888/event' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 201,
  "event_date": "2012-07-02T22:05:22",
  "attribute1": 2,
  "attribute2": 2,
  "attribute3": 3,
  "attribute4": "test-post",
  "attribute5": "12345",
  "attribute6": false,
  "metric1": 12,
  "metric2": 5.5
}'
# GET-3
echo "\n get-3"
curl -X 'GET' \
  'http://localhost:8888/analytics/query?metrics=metric1%2Cmetric2&groupBy=attribute5%2Cattribute2&filters=attribute%3Aattribute3%2Cvalue%3A1&filters=attribute%3Aattribute4%2Cvalue%3Atest&granularity=hourly' \
  -H 'accept: application/json'

