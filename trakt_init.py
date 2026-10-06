#!/usr/bin/env python3
# irbyjm 20180929

from getpass import getpass
from sys import argv
from time import monotonic, sleep
import trakt
from trakt.auth.device import DeviceAuthAdapter
from trakt.errors import BadRequestException, RateLimitException, TraktException

# make sure username is specified so it's not stored somewhere hard
if len(argv) != 2:

    # dump if username not specified
    print("Usage: ./trakt_init.py [username]")
else:

    # else go to town
    username = argv[1]
    print("Create or view your Trakt API app at https://app.trakt.tv/oauth/applications")
    client_id = getpass("Please enter your client id: ").strip()
    client_secret = getpass("Please enter your client secret: ").strip()
    if not client_id or not client_secret:
        print("Both the client ID and client secret are required.")
        exit(1)

    # Device authentication avoids the obsolete browser redirect. Use the
    # low-level methods because PyTrakt's helper prints access tokens.
    config = trakt.core.config()
    config.update(CLIENT_ID=client_id, CLIENT_SECRET=client_secret)
    auth = DeviceAuthAdapter(client=trakt.core.api(), config=config)
    device = auth.get_device_code()
    deadline = monotonic() + device["expires_in"]
    interval = device["interval"]
    print("Approve this code in your browser while signed in as", username)

    while monotonic() < deadline:
        sleep(max(0, min(interval, deadline - monotonic())))
        if monotonic() >= deadline:
            continue
        try:
            auth.get_device_token(device["device_code"])
        except BadRequestException:
            # HTTP 400 means approval is still pending.
            continue
        except RateLimitException:
            interval *= 2
            continue
        except TraktException as error:
            print(f"Trakt authorization failed (HTTP {error.http_code}). Please retry.")
            exit(1)

        #information stored in ~/.pytrakt.json
        config.store()
        print("Successfully authenticated with Trakt.")
        break
    else:
        print("The login code expired. Run this script again.")
        exit(1)
