#!/usr/bin/env python3
# irbyjm 20180929

from sys import argv
from trakt.users import User
import time
from calendar import timegm
import discordrpc
from discordrpc import Activity
import os
import signal

def signal_handler(sig, frame):
    runtime = round((time.time() - start)/60/60, 2)
    print('\n', time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ': Ctrl+C pressed; exiting after', runtime, 'hours')
    try:
        rpc_obj.disconnect()
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
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Successfully connected to Trakt")
        except Exception:
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt connection failure")
            time.sleep(15)

    client_id = argv[2]
    try:
        rpc_obj = discordrpc.RPC(
                app_id=client_id,
                output=False,
                debug=False
        )
        print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Successfully connected to Discord")
    except ConnectionRefusedError:
        print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Discord connection failure")
        exit(0)

    while True:
        try:
            watching = my.watching
            if watching:
                timestamp = int(timegm(time.strptime(watching.started_at, "%Y-%m-%dT%H:%M:%S.000Z")))
                
                if watching.media_type == "episodes":
                    details = watching.show
                    state = "".join(("S", str(watching.season), "E", str(watching.episode), " (", watching.title  , ")"))
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: playing", details, state)
                else:
                    details = watching.title
                    state = f"({watching.year})"
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: playing", details, state)
                try:
                    rpc_obj.set_activity(
                        details=details,
                        state=state,
                        ts_start=timestamp,
                        small_text="Playing",
                        small_image="play",
                        large_text="Trakt",
                        large_image="trakt",
                        act_type=Activity.Watching
                    )
                    # print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": DEBUG : Sending data to Discord")
                except:
                    try:
                        rpc_obj = discordrpc.RPC(
                            app_id=client_id,
                            output=False,
                            debug=False
                        )
                        print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Successfully connected to Discord")
                    except:
                        print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Discord connection failure")

            else:
                try:
                    # Figure out if this is actually sending Trakt something
                    # If it's not actually sending packets to Trakt
                    # Then I don't particularly care
                    print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": Trakt: not playing")
                    rpc_obj.clear()
                except:
                    pass
        except:
            print(time.strftime("%Y-%m-%dT%H:%M:%S.000%Z"), ": General failure")
        time.sleep(15)
