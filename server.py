#!/usr/bin/env python

import asyncio
import signal
import os
import signal
import websockets
import httpx

async def get_json_from_url(url):
  async with httpx.AsyncClient() as client:
    response = await client.get(url)
    return response.content.decode("utf-8")

async def echo(websocket):
    async for message in websocket:
        if message.startswith("visuals"):
          await websocket.send(await get_json_from_url("https://api.mads.monster/visuals"))
        elif message.startswith("toptexts"):
          await websocket.send(await get_json_from_url("https://api.mads.monster/toptexts/"))
        elif message.startswith("bottomtexts"):
          await websocket.send(await get_json_from_url("https://api.mads.monster/bottomtexts"))
        else:
          await websocket.send(message)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    signal.signal(signal.SIGTERM, lambda *args: loop.stop())
    signal.signal(signal.SIGINT, lambda *args: loop.stop())
    listen_port = int(os.environ.get("PORT", 5678))
    async with websockets.serve(
        echo,
        host="",
        port=listen_port,
    ):
      print(f"Listing on {listen_port}")
      await stop


if __name__ == "__main__":
    asyncio.run(main())