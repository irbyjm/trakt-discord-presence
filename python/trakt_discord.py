#!/usr/bin/env python
# irbyjm 20180929

from sys import argv
from trakt.users import User
import time

if len(argv) != 2:

    print("Usage: ./trakt_discord.py [username]")
else:
    username = argv[1]
    my = User(username)
    
    while True:
        if my.watching:
            print("Trakt: playing ", my.watching.show)
        else:
            print("Trakt: not playing")
        time.sleep(15)
