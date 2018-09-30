#!/usr/bin/env python3
# irbyjm 20180929

from sys import argv
from trakt.users import User
import time
import rpc
import os

if len(argv) != 3:
    print("Usage: ./trakt_discord.py [username] [Discord_client_ID]")
else:
    username = argv[1]
    my = User(username)
    client_id = argv[2]
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    os.environ['TZ']='UTC'
    time.sleep(5)
    
    while True:
        if my.watching:
            timestamp = int(time.mktime(time.strptime(my.watching.started_at[:-1]+"UTC", "%Y-%m-%dT%H:%M:%S.000%Z")))
            activity = {
                    "timestamps": {
                        "start": timestamp
                    },
                    "assets": {
                        "small_text": "Playing",
                        "small_image": "play",
                        "large_text": "Trakt",
                        "large_image": "trakt"
                    }
            }
            
            if "Movie" in str(my.watching.__class__):
                details  = "".join((my.watching.title, " (", str(my.watching.year), ")"))
                activity["details"] = details
                print("Trakt: playing", details)
            else:
                details = my.watching.show
                state = "".join(("S", str(my.watching.season), "E", str(my.watching.episode), " (", my.watching.title  , ")"))
                activity["details"] = details
                activity["state"] = state
                print("Trakt: playing", details, state)
            try:
                rpc_obj.set_activity(activity)
            except:
                rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
        else:
            try:
                print("Trakt: not playing")
                rpc_obj.close()
            except:
                pass
        time.sleep(30)
