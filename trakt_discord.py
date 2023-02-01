#!/usr/bin/env python3
# irbyjm 20180929

import config
from sys import argv
from trakt.users import User
import time
from calendar import timegm
import libs.rpc as rpc
import os
import signal

def signal_handler(sig, frame):
    runtime = round((time.time() - start)/60/60, 2)
    print('\n', time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ': Ctrl+C pressed; exiting after', runtime, 'hours')
    try:
        rpc_obj.close()
    except:
        pass
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

start = time.time()

if len(argv) != 1:
    print("Usage: ./trakt_discord.py [username] [Discord_client_ID]")
else:
    username = config.username

    trakt_connected = False
    while not trakt_connected:
        try:
            my = User(username)
            trakt_connected = True
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Successfully connected to Trakt")
        except Exception:
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt Connection Failure (1)")
            time.sleep(15)

    client_id = argv[2]
    # force this script to live on an island and catch the errors
    # I don't want to see a command prompt when I'm expecting this to keep going
    # Spit an error for OSError: [Errno 107] Transport endpoint is not connecte
    # Discord has to be running before this is--duh
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)

    while True:
        try:
            watching = my.watching
            if watching:
                timestamp = int(timegm(time.strptime(watching.started_at, "%Y-%m-%dT%H:%M:%S.000Z")))
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

                if watching.media_type == "episodes":
                    details = watching.show
                    state = "".join(("S", str(watching.season), "E", str(watching.episode), " (", watching.title  , ")"))
                    activity["details"] = details
                    activity["state"] = state
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: playing", details, state)
                else:
                    details  = "".join((watching.title, " (", str(watching.year), ")"))
                    activity["details"] = details
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: playing", details)
                try:
                    rpc_obj.set_activity(activity)
                    # print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": DEBUG : Sending data to Discord")
                except:
                    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
            else:
                try:
                    # Figure out if this is actually sending Trakt something
                    # If it's not actually sending packets to Trakt
                    # Then I don't particularly care
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: not playing")
                    rpc_obj.close()
                except:
                    pass
        except:
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt Connection Failure (2)")
        time.sleep(15)
