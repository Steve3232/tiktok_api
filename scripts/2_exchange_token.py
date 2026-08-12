#!/usr/bin/env python3
"""
Step 2 of the demo flow: exchange the authorization code (from the
callback.html URL) for an access token, and save it to token.json
(gitignored — never commit this file).

Usage:
    TIKTOK_CLIENT_KEY=... TIKTOK_CLIENT_SECRET=... python3 2_exchange_token.py \
        "https://steve3232.github.io/tiktok_api/callback.html?code=...&state=..."
"""
import json
import os
import sys
import urllib.parse
import urllib.request

CLIENT_KEY = os.environ["TIKTOK_CLIENT_KEY"]
CLIENT_SECRET = os.environ["TIKTOK_CLIENT_SECRET"]
REDIRECT_URI = "https://steve3232.github.io/tiktok_api/callback.html"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")

if len(sys.argv) != 2:
    sys.exit("Usage: python3 2_exchange_token.py '<full callback URL>'")

callback_url = sys.argv[1]
query = urllib.parse.urlparse(callback_url).query
code = urllib.parse.parse_qs(query).get("code", [None])[0]
if not code:
    sys.exit("No `code` param found in that URL — did the redirect happen correctly?")

data = urllib.parse.urlencode({
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}).encode()

req = urllib.request.Request(
    "https://open.tiktokapis.com/v2/oauth/token/",
    data=data,
    headers={"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"},
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    result = json.load(resp)

if "access_token" not in result:
    sys.exit(f"Token exchange failed: {result}")

with open(TOKEN_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(f"Access token saved to {TOKEN_PATH}")
print(f"Open ID: {result.get('open_id')}")
print(f"Expires in: {result.get('expires_in')}s")
