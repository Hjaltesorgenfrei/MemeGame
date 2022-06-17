#!/usr/bin/env python

import asyncio
import signal
import json
import os
import websockets.server
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
    return json.dumps([{'key': k, 'value': dic[k]} for k in dic])

def filter_images(name):
    if not name:
        return False 
    l = name.lower()
    return l.endswith("png") or l.endswith("jpg") or l.endswith("jpeg")

visuals = {x["id"]: x["filename"]
           for x in get_json_from_url("https://api.mads.monster/visuals") if filter_images(x['filename']) }
top_texts = {x["id"]: x["memetext"]
             for x in get_json_from_url("https://api.mads.monster/toptexts")}
bottoms_texts = {x["id"]: x["memetext"]
                 for x in get_json_from_url("https://api.mads.monster/bottomtexts")}

print(visuals)

connections = []

async def receive_messages(websocket):
    connections.append(websocket)
    async for message in websocket:
        try:
            data = json.loads(message)
        except:
            print("Failed on:", message)
            continue
        match (data["type"]):
            case "username_change_request": 
                response = json.dumps({
                    "type":"username_change_approve",
                    "username": data["username"],
                    "user_id": data["user_id"]
                    })
                websockets.broadcast(connections, response)
                print(data["user_id"], "changed name to", data["username"])
            case _:
                print(data)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    signal.signal(signal.SIGTERM, lambda *args: loop.stop())
    signal.signal(signal.SIGINT, lambda *args: loop.stop())
    listen_port = int(os.environ.get("PORT", 5678))
    async with websockets.server.serve(
        receive_messages,
        host="",
        port=listen_port,
    ):
        print(f"Listing on {listen_port}")
        await stop


if __name__ == "__main__":
    asyncio.run(main())
