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

    trakt_connected = 0
    while trakt_connected == 0:
        try:
            my = User(username)
            trakt_connected = 1
            print("Successfully connected to Trakt")
        except Exception:
            print("Trakt Connection Failure")
            time.sleep(15)

    client_id = argv[2]
    # Same thing here; attempt to force this script to live while on an island
    # I don't want to see a command prompt when I'm expecting this to keep going
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    os.environ['TZ']='UTC'
    time.sleep(5)

    while True:
        if my.watching:
            # my.watching may have turned into NoneType at some point and died
            # this caused timetamp to fail because started_at was invalid
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
                # Figure out how to set a sentinel on this
                # We don't need to change this every 15 seconds
                rpc_obj.set_activity(activity)
            except:
                rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
        else:
            try:
                # Figure out if this is actually sending Trakt something
                # If it's not actually sending packets to Trakt if it's not
                # Then I don't particularly care
                print("Trakt: not playing")
                rpc_obj.close()
            except:
                pass
        time.sleep(15)
