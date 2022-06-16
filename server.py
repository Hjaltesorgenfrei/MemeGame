#!/usr/bin/env python

import asyncio
import signal
import json
import os
import websockets
import httpx
import requests

async def get_json_from_url_async(url):
  async with httpx.AsyncClient() as client:
    response = await client.get(url)
    return json.loads(response.content.decode("utf-8"))

def get_json_from_url(url):
  response = requests.get(url)
  return json.loads(response.content.decode("utf-8"))

def json_array_from_dict(dic):
  return json.dumps([{'key' : k, 'value' : dic[k]} for k in dic])

visuals = {x["id"]:x["filename"] for x in get_json_from_url("https://api.mads.monster/visuals")}
top_texts = {x["id"]:x["memetext"] for x in get_json_from_url("https://api.mads.monster/toptexts")}
bottoms_texts = {x["id"]:x["memetext"] for x in get_json_from_url("https://api.mads.monster/bottomtexts")}

print(json_array_from_dict(bottoms_texts))



async def echo(websocket):
    async for message in websocket:
        if message.startswith("visuals"):
          await websocket.send(json_array_from_dict(visuals))
        elif message.startswith("toptexts"):
          await websocket.send(json_array_from_dict(top_texts))
        elif message.startswith("bottomtexts"):
          await websocket.send(json_array_from_dict(bottoms_texts))
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