#!/usr/bin/env python

import asyncio
import signal
import os
import signal
import websockets


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    signal.signal(signal.SIGTERM, lambda *args: loop.stop())
    signal.signal(signal.SIGINT, lambda *args: loop.stop())
    listen_port = int(os.environ.get("PORT", 5678))
    async with websockets.serve(
        echo,
        host="",
        port= listen_port,
    ):
      print(f"Listing on {listen_port}")
      await stop


if __name__ == "__main__":
    asyncio.run(main())