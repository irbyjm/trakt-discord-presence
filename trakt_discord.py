#!/usr/bin/env python3
# irbyjm 20180929

from sys import argv
from trakt.users import User
import time

if len(argv) != 3:

    print("Usage: ./trakt_discord.py [username] [Discord_client_ID")
else:
    username = argv[1]
    my = User(username)
    
    while True:
        if my.watching:
            if "Movie" in str(my.watching.__class__):
                print("Trakt: playing ", my.watching.title, " (", my.watching.year, ")")
            else:
                print("Trakt: playing ", my.watching.show, " (S", my.watching.season, "E", my.watching.episode, ")", sep='')
        else:
            print("Trakt: not playing")
        time.sleep(15)
