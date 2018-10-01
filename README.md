# trakt-discord-presence
Update your Discord status based on movies you are watching on Trakt.tv .

_Some assets sourced from: https://github.com/suclearnub/python-discord-rpc/ and https://github.com/matthewdias/trakt-discord-presence_

## Requirements
- Trakt.tv account
- Trakt.tv App API Key
- Discord App API Key

## Installation
# Python
Install all relevant Python 3 packages to connect Trakt.tv and Discord (`sudo` as neccessary):

```pip3 install discord trakt```

# Trakt
Create a Trakt API App named "Discord" and set the following Redirect URI for OAuth:

```urn:ietf:wg:oauth:2.0:oob```

Record the Client ID and Client Secret for initializing the Trakt API module. Using this information and your Trakt username, run `trakt_init.py`, receiving a PIN from Trakt at the end:
```
[user@host trakt-discord-presence]$ ./trakt_init.py <trakt username>
If you do not have a client ID and secret. Please visit the following url to create them.
http://trakt.tv/oauth/applications
Please enter your client id: <client id>
Please enter your client secret: <client secret>
Please go here and authorize, https://api-v2launch.trakt.tv/oauth/authorize?response_type=code&client_id=...
Paste the Code returned here: <trakt code>
```
