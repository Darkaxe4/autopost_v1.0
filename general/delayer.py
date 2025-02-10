import asyncio
from datetime import datetime, timedelta
from typing import Callable

# Define a callback function
def my_callback():
    print(f"Callback executed at {datetime.now().timestamp()}")

class Delayer:
    def __init__ (self):
        self.loop = asyncio.get_event_loop()

    async def delayFunction(self, time:datetime, func:Callable):
        now = self.loop.time()
        timedelay = time - datetime.now()
        timestamp = now + timedelay.total_seconds()
        self.loop.call_at(timestamp, func)

async def main():

    bubylda = Delayer()
    await bubylda.delayFunction(datetime.now()+timedelta(seconds=5), my_callback)

    # Keep the event loop running for a while to allow the callback to execute
    while True:
        await asyncio.sleep(1)  # Wait longer than the scheduled time

# Run the asyncio event loop
asyncio.run(main())