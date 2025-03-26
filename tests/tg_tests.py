from datetime import datetime, timedelta
import sys
import os
from asyncio import sleep, run
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tg_bot.tg_api import send_post
from general.delayer import delayer
from general.logger import logger
from general.config_parser import parser

async def main():
    delayer()
    parser()
    logger("general/config.ini")
    time = datetime.now() + timedelta(seconds=5)
    await delayer.instance.delayFunction(time, send_post("Test message", time))
    await sleep(10)

if __name__ == "__main__":
    run(main())

