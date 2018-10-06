#!/usr/bin/env python3
# irbyjm 20180929

from sys import argv
from trakt.users import User
import time
import rpc
import os
import signal

def signal_handler(sig, frame):
    runtime = round((time.time() - start)/60/60, 2)
    print('\n** Ctrl+C pressed; exiting after', runtime, 'hours')
    try:
        rpc_obj.close()
    except:
        pass
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

start = time.time()

if len(argv) != 3:
    print("Usage: ./trakt_discord.py [username] [Discord_client_ID]")
else:
    username = argv[1]

    trakt_connected = False
    while not trakt_connected:
        try:
            my = User(username)
            trakt_connected = True
            print("** Successfully connected to Trakt")
        except Exception:
            print("** Trakt Connection Failure")
            time.sleep(15)

    client_id = argv[2]
    # force this script to live on an island and catch the errors
    # I don't want to see a command prompt when I'm expecting this to keep going
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    os.environ['TZ']='UTC'
    time.sleep(5)

    while True:
        try:
            watching = my.watching
            if watching:
                timestamp = int(time.mktime(time.strptime(watching.started_at[:-1]+"UTC", "%Y-%m-%dT%H:%M:%S.000%Z")))
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

                if "Movie" in str(watching.__class__):
                    details  = "".join((watching.title, " (", str(watching.year), ")"))
                    activity["details"] = details
                    print("Trakt: playing", details)
                else:
                    details = watching.show
                    state = "".join(("S", str(watching.season), "E", str(watching.episode), " (", watching.title  , ")"))
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
        except:
            print("** Trakt Connection Failure")
        time.sleep(15)
