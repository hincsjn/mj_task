import sys
import json
import time
import requests
import websocket
import redis
import os

status = "online"

custom_status = "" #If you don't need a custom status on your profile, just put "" instead of "youtube.com/@SealedSaucer"

usertoken = "MTA5MTU0NzI0NDI5OTI4ODY2Ng.GMaoTA.5KH_NZeSoLC-9hy1Owa7VgljEboJ0ZtV3u90cg"

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]


# r = redis.Redis(
#     host='0.0.0.0',
#     port=6379,
#     password="123",
#     decode_responses=True
# )
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    # password="123",
    decode_responses=True
)


def connect(ws, token):
    print('============ПЕРЕЗАПУСК=============')

    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))


def onliner(token, status):
    ws = websocket.WebSocket()
    connect(ws, token)
    cstatus = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": custom_status,
                    "name": "Custom Status",
                    "id": "custom",
                    #Uncomment the below lines if you want an emoji in the status
                    #"emoji": {
                        #"name": "emoji name",
                        #"id": "emoji id",
                        #"animated": False,
                    #},
                }
            ],
            "status": status,
            "afk": False,
        },
    }
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": "None"}
    while True:
        try:
            message = json.loads(ws.recv())
            try:
                if message["t"] in ["MESSAGE_CREATE", "MESSAGE_UPDATE"]:
                    print(message['d']['content'])
            except:
                ...
            r.publish("mj-response", ws.recv())
        except websocket.WebSocketConnectionClosedException:
            connect(ws, token)
        except:
            ...

def run_onliner():
    # os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(usertoken, status)
        time.sleep(10)

if __name__ == '__main__':
    run_onliner()
