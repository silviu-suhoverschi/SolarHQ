"""
Entry point for the standalone scheduler process.
Used by s6 longrun service solarhq-scheduler.
"""
import asyncio
import signal
from .scheduler import start_scheduler


async def main():
    scheduler = start_scheduler()

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    loop.add_signal_handler(signal.SIGINT, stop_event.set)

    await stop_event.wait()
    scheduler.shutdown(wait=False)


if __name__ == "__main__":
    asyncio.run(main())
