
import asyncio
import json
import logging
import websockets
import random
import string

USERS = list()


def startWS():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig()
    addr = "127.0.0.1"
    port = 4200
    start_server = websockets.serve(counter, addr, port)
    print("websocket server's running on "+str(addr)+":"+str(port))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def findClient(id, userList):
    for user in userList:
        if user['socketID'] == id:
            return user['socket']


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))


def state_event():
    return json.dumps({"type": "state"})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()

        await asyncio.wait([user['socket'].send(message) for user in USERS])


async def notify_users(id):
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps({"type": "message",
                              "content": "user " + id + " has been connected"})
        await asyncio.wait([user['socket'].send(message) for user in USERS])


async def login(websocket, id):
    USERS.append({"socketID": id, "socket": websocket})
    await websocket.send(json.dumps({"type": "connect", "id": id}))
    await notify_users(id)


async def unlogin(websocket, id):
    USERS.remove({"socketID": id, "socket": websocket})
    await notify_users(id)


async def counter(websocket, path):
    # login(websocket) sends user_event() to websocket
    socketID = randomString(10)
    await login(websocket, socketID)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            sk = findClient(data['username'], USERS)
            await sk.send(message)
    finally:
        await unlogin(websocket, socketID)


def handleRequest(data: dict):
    if data['type'] == "offer":
        pass
    elif data['type'] == "answer":
        pass
    elif data['type'] == "candidate":
        pass
    elif data['type'] == "offer":
        pass
    return json.dumps(data)
