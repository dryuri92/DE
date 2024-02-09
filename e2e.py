#DEBUG MODULE
import asyncio
import asyncpg
from datetime import datetime
from typing import List
from random import randrange
import random
from datetime import timedelta
import timeit
import aiohttp

start = "2011-01-01T08:00:00"
end = "2012-12-12T18:55:59"
#datetime_object = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generateRecord(number: int)->List[tuple]:
    values = []
    for i in range(number):
        values.append(
            (
            i+1,
            random_date(start_date, end_date),
            randrange(0,9),
            randrange(0,9),
            randrange(0,9),
            f"test {i}",
            "raw",
            bool(randrange(0,1),
            ),
            randrange(1,1000),
            round(random.random()*10, 2)))
    return values

async def run():
    conn = await asyncpg.connect(user='root', password='root',port=5432,
                                 database='test_db', host='localhost')
    print(f"connectiion is {conn}")
    if (conn):
        await conn.execute('DELETE FROM cd.events')
        l = generateRecord(100000)
        print(l[1])
        await conn.copy_records_to_table(
            'events', records=l, schema_name="cd",
            columns=['id','event_date','attribute1','attribute2','attribute3','attribute4','attribute5','attribute6','metric1','metric2'])
        print(len(l))
       
#
async def once():
    req = 'http://localhost:8888/analytics/query?metrics=metric1%2Cmetric2&groupBy=attribute1%2Cattribute2&filters=attribute%3Aattribute5%2Cvalue%3Araw&granularity=hourly&startDate=2011-07-03T08%3A00%3A00&endDate=2012-07-03T11%3A21%3A00'
    async with aiohttp.ClientSession() as session:
        async with session.get(req) as resp:
            assert resp.status == 200
            data = await resp.json()
            print(len(data))
async def main():
    await run()
    await once()

print(timeit.timeit('asyncio.run(main())', globals=globals(), number=1))