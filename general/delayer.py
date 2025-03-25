import asyncio
from datetime import datetime, timedelta
from typing import Callable
from collections import defaultdict

from general.logger import logger
from general.utils import singletone

class Delayer(singletone):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.scheduled_tasks = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def delayFunction(self, time: datetime, func: Callable, priority: int = 0):
        async with self.lock:
            now = self.loop.time()
            timedelay = time - datetime.now()
            timestamp = now + timedelay.total_seconds()

            self.scheduled_tasks[timestamp].append((priority, func))
            self.scheduled_tasks[timestamp].sort(key=lambda x: -x[0])

            self.loop.call_at(timestamp, self._execute_scheduled_tasks, timestamp)
    
    def _execute_scheduled_tasks(self, timestamp):
        if timestamp in self.scheduled_tasks:
            tasks = self.scheduled_tasks[timestamp]
            for priority, func in tasks:
                try:
                    if asyncio.iscoroutinefunction(func):
                        self.loop.create_task(func())
                    else:
                        func()
                except Exception as e:
                    logger.instance.log('Error executing scheduled task:', e)
            del self.scheduled_tasks[timestamp]

    async def cancelScheduled(self, time: datetime):
        timestamp = self.loop.time() + (time - datetime.now()).total_seconds()
        if timestamp in self.scheduled_tasks:
            del self.scheduled_tasks[timestamp]