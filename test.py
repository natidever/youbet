import asyncio

async def test():
    for i in range(1,10):
        print(f"number:{i}")
        await asyncio.sleep(1)


asyncio.run(test())



   
