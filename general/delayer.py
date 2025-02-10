import asyncio
from datetime import datetime, timedelta

# Define a callback function
def my_callback():
    print(f"Callback executed at {datetime.now().timestamp()}")

async def main():
    # Get the event loop
    loop = asyncio.get_event_loop()

    # Get the current time
    now = loop.time()
    loop.time()
    print(now)

    # Schedule the callback to run 5 seconds from now
    timestamp = now + 5
    loop.call_at(timestamp, my_callback)

    print(f"Scheduled callback to run at {timestamp}")

    # Keep the event loop running for a while to allow the callback to execute
    await asyncio.sleep(6)  # Wait longer than the scheduled time

# Run the asyncio event loop
asyncio.run(main())