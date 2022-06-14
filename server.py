#!/usr/bin/env python

import asyncio
import websockets

SERVER_ADDRESS = '127.0.0.1'
HTTP_PORT = 80
WEBSOCKET_PORT = 5678


async def handle_http(reader, writer):
  data = await reader.read(100)
  message = data.decode()
  writer.write(data)
  await writer.drain()
  writer.close()


async def ws_callback(websocket, path):
  global parsed_data
  while True:
      data = await websocket.recv()
      # How do I access parsed_data in the main function below
      # parsed_data = json.loads(data)
      await websocket.send(data)

async def main():
  ws_server = await websockets.serve(ws_callback, SERVER_ADDRESS, WEBSOCKET_PORT)
  print(f'Websocket server listening on port {WEBSOCKET_PORT}')
  http_server = await asyncio.start_server(
      handle_http, SERVER_ADDRESS, HTTP_PORT)
  print(f'HTTP server listening on port {HTTP_PORT}')
  await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())