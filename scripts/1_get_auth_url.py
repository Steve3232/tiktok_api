#!/usr/bin/env python3
"""
Step 1 of the demo flow: print the TikTok authorization URL to open in a
browser. Run this, open the printed URL, log in, and approve — TikTok
redirects to callback.html, which shows the full redirected URL (with the
`code` param) in a copy-able box.

Usage:
    TIKTOK_CLIENT_KEY=... python3 1_get_auth_url.py
"""
import os
import secrets
import urllib.parse

CLIENT_KEY = os.environ["TIKTOK_CLIENT_KEY"]
REDIRECT_URI = "https://steve3232.github.io/tiktok_api/callback.html"
SCOPES = "user.info.basic,video.upload"

state = secrets.token_urlsafe(16)
params = {
    "client_key": CLIENT_KEY,
    "scope": SCOPES,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "state": state,
}
url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(params)

print("Open this URL, log in, and approve access:\n")
print(url)
print(f"\n(state = {state} — you don't need this, just here for reference)")
