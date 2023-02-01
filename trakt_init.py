#!/usr/bin/env python3

from sys import argv
import config
import trakt

# make sure username is specified so it's not stored somewhere hard
if len(argv) != 1:

    # dump if username not specified
    print("Usage: $ python trakt_init.py")
else:

    # else go to town
    username = config.username

    # AUTH_METHOD defaults to PIN which has been deprecated
    trakt.core.AUTH_METHOD=trakt.core.OAUTH_AUTH

    #information stored in ~/.pytrakt.json
    trakt.init(username, store=True)
