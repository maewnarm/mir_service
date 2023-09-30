import threading as th
import multiprocessing as mp
import asyncio
import rel
import websocket
from websockets.server import serve
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed

ws_client = None


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


def ws_connect():
    global ws_client
    ws_client = websocket.WebSocketApp(
        "ws://localhost:1880",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    try:
        ws_client.run_forever(dispatcher=rel, reconnect=5)
    except KeyboardInterrupt:
        pass
    # thr = th.Thread(target=ws_client.run_forever(dispatcher=rel, reconnect=5))
    # thr.start()
    # rel.signal(2, rel.abort)
    # rel.dispatch()


async def echo(websocket):
    global ws_client
    async for message in websocket:
        print(message)
        if ws_client is not None:
            ws_client.send(message)


async def ws_serve():
    async with serve(echo, "localhost", 1881):
        print("served")
        ws_connect()
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        serve_ws = mp.Process(target=asyncio.run(ws_serve()))
        connect_ws = mp.Process(target=ws_connect())
        connect_ws.start()
        # start process
        serve_ws.start()
    except KeyboardInterrupt:
        pass
