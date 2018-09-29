#!/usr/bin/env python3
# irbyjm 20180929

from sys import argv
import trakt

# make sure username is specified so it's not stored somewhere hard
if len(argv) != 2:

    # dump if username not specified
    print("Usage: ./trakt_init.py [username]")
else:

    # else go to town
    username = argv[1]

    # AUTH_METHOD defaults to PIN which has been deprecated
    trakt.core.AUTH_METHOD=trakt.core.OAUTH_AUTH

    #information stored in ~/.pytrakt.json
    trakt.init(username, store=True)
