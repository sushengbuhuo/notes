import aiohttp
import asyncio,httpx
from datetime import datetime

#http://www.justdopython.com/2019/12/27/python-aiohttp-102/ https://github.com/JustDoPython/python-100-day/tree/master/day-102
async def fetch(client):
    async with client.get('http://httpbin.org/get') as resp:
        assert resp.status == 200
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)
async def main2():
    async with aiohttp.ClientSession() as client:
       tasks = []
       for i in range(30):
           tasks.append(asyncio.create_task(fetch(client)))
       await asyncio.wait(tasks)
loop = asyncio.get_event_loop()

tasks = []
for i in range(10):
    task = loop.create_task(main())
    tasks.append(task)

start = datetime.now()

loop.run_until_complete(main())

# loop.run_until_complete(main2())
end = datetime.now()

print("aiohttp版爬虫花费时间为：")
print(end - start)
