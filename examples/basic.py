import asyncio
from crono import Crono

crono = Crono()

@crono.every(minutes=5, args=('World',))
def hello_world(name):
    print(f"Hello, {name}!")

@crono.every(minutes=10, args=(42,))
async def async_count(number):
    await asyncio.sleep(1)
    print(f"Counted to {number}")

if __name__ == "__main__":
    hello_world("World")  # Test sync task
    asyncio.run(async_count(42))  # Test async task
    crono.write_crontab(filename="basic_crontab")