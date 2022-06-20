#!/usr/bin/env python

import asyncio
import signal
import json
import os
import websockets.server
import websockets
import httpx
import requests

class Game():
    def __init__(self, host_id) -> None:
        self.visuals = {x["id"]: x["filename"]
           for x in get_json_from_url("https://api.mads.monster/visuals") if filter_images(x['filename']) }
        self.top_texts = {x["id"]: x["memetext"]
                    for x in get_json_from_url("https://api.mads.monster/toptexts")}
        self.bottoms_texts = {x["id"]: x["memetext"]
                        for x in get_json_from_url("https://api.mads.monster/bottomtexts")}
        self.host_id = host_id
        pass

class Player():
    def __init__(self, user_id, username) -> None:
        self.user_id = user_id
        self.username = username
        pass

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

players = {}
current_game = None

connections = []

async def receive_messages(websocket):
    global current_game
    connections.append(websocket)
    async for message in websocket:
        try:
            data = json.loads(message)
        except:
            print("Failed on:", message)
            continue
        user_id = data["user_id"]
        match (data["type"]):
            case "username_change_request": 
                response = json.dumps({
                    "type":"username_change_approve",
                    "username": data["username"],
                    "user_id": user_id
                    })
                websockets.broadcast(connections, response)
                print(user_id, "changed name to", data["username"])
            case "user_joined":
                if user_id not in players:
                    players[user_id] = Player(user_id, data["username"])  
                    print(f'New player joined {user_id} {data["username"]}')    
                else:
                    print(f'Rejoined player joined {user_id} {data["username"]}')
                if current_game:
                    response = json.dumps({
                        "type":"game_in_progress",
                        "host": players[current_game.host_id].username,
                    })
                    await websocket.send(response)
            case "start_game":
                if current_game:
                    await websocket.send(json.dumps({
                        "type":"error",
                        "message": "Game was already started"
                    }))
                    continue

                current_game = Game(user_id)
                response = json.dumps({
                    "type":"game_started",
                    "host": players[user_id].username,
                })
                websockets.broadcast(connections, response)
                print("Started new game")
            case "end_game":
                current_game = None
                response = json.dumps({
                    "type":"game_ended",
                })
                websockets.broadcast(connections, response)
                print("Ended game")
            case _:
                print(data)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    signal.signal(signal.SIGTERM, lambda *args: stop.set_result(None))
    signal.signal(signal.SIGINT, lambda *args: stop.set_result(None))
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
