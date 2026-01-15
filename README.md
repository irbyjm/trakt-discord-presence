# Trakt 'Watching' Discord Rich Presence
Update your Discord status based on movies you are watching on Trakt.tv .

_Some assets sourced from: https://github.com/mitgobla/python-discord-rpc/ and https://github.com/matthewdias/trakt-discord-presence_

## Requirements
- Trakt.tv account
- Trakt.tv App API Key
- Discord App API Key
- Local Discord client for RPC connectivity

## Installation
Install all relevant Python 3 packages to connect Trakt.tv and Discord (`sudo` as neccessary):

```pip3 install pytrakt discord-rpc```

## Getting Started
### Trakt
Create a Trakt API App (https://trakt.tv/oauth/applications) named "Discord" and set the following Redirect URI for OAuth:

```urn:ietf:wg:oauth:2.0:oob```

Record the Client ID and Client Secret for initializing the Trakt API module. Using this information and your Trakt username, run `trakt_init.py`, receiving a PIN from Trakt at the end (requires sign-in):
```
[user@host trakt-discord-presence]$ ./trakt_init.py <trakt username>
If you do not have a client ID and secret. Please visit the following url to create them.
http://trakt.tv/oauth/applications
Please enter your client id: <client id>
Please enter your client secret: <client secret>
Please go here and authorize, https://api.trakt.tv/oauth/authorize?response_type=code&...
Paste the Code returned here: <trakt code>
```

This will cause Trakt API information to be stored in `~/.pytrakt.json` for future reference.

### Discord
Create a Discord API App (https://discordapp.com/developers/applications/) named "Trakt" and record the Discord Client ID for authorizing the trakt-discord application.

Navigate to <Application Settings/Rich Presence/Art Assets> and upload the three icons found in `icons/`.

Configure the Discord app as follows:

Area | Option | Setting
---- | ------ | -------
General Information | App Icon | icons/large/trakt.png
Rich Presence | Large Image Key | trakt
Rich Presence | Small Image Key | play
Art Assets | Cover Image | icons/large/trakt.png

## Usage
The Trakt-Discord connector may be ran directly or called via another script for ease-of-use. The application may be ran directly as so:
````
[user@host trakt-discord-presence] ./trakt_discord.py <trakt username> <discord client id>
````

To not have to keep referencing the Discord Client ID manually, this may be scripted as:
````bash
#!/bin/bash

./trakt_discord.py <trakt username> <discord client id>
````

If the above steps were successful, output similar to the following should be visible (assuming the user is not currently checked in on Trakt; and assuming a bash script was created named `watch.sh`):
````
[user@host trakt-discord-presence] ./watch.sh
** Successfully conected to Trakt
Trakt: not playing
````

This script may then run on startup, if desired.
