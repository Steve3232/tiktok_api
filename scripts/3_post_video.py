#!/usr/bin/env python3
"""
Step 3 of the demo flow: post a video to TikTok as a private (SELF_ONLY)
draft via the Content Posting API, using push_by_file (direct upload).

Unaudited apps can only post as SELF_ONLY (visible only to the account
owner, in their TikTok inbox for review) — that's a TikTok platform
restriction, not a limitation of this script. Once the app is approved,
change PRIVACY_LEVEL below.

Usage:
    python3 3_post_video.py /path/to/video.mp4 "Caption text here"
"""
import json
import os
import sys
import urllib.request

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")
PRIVACY_LEVEL = "SELF_ONLY"  # unaudited apps must use this

if len(sys.argv) != 3:
    sys.exit("Usage: python3 3_post_video.py <video_path> '<caption>'")

video_path = sys.argv[1]
caption = sys.argv[2]

with open(TOKEN_PATH) as f:
    token_data = json.load(f)
access_token = token_data["access_token"]

video_size = os.path.getsize(video_path)

init_body = json.dumps({
    "post_info": {
        "title": caption,
        "privacy_level": PRIVACY_LEVEL,
        "disable_duet": False,
        "disable_comment": False,
        "disable_stitch": False,
        "video_cover_timestamp_ms": 1000,
    },
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size,
        "chunk_size": video_size,
        "total_chunk_count": 1,
    },
}).encode()

req = urllib.request.Request(
    "https://open.tiktokapis.com/v2/post/publish/video/init/",
    data=init_body,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
    },
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    init_result = json.load(resp)

print("Init response:", json.dumps(init_result, indent=2))

data = init_result.get("data", {})
upload_url = data.get("upload_url")
publish_id = data.get("publish_id")
if not upload_url:
    sys.exit("No upload_url returned — check the init response above for the error.")

with open(video_path, "rb") as f:
    video_bytes = f.read()

put_req = urllib.request.Request(
    upload_url,
    data=video_bytes,
    headers={
        "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
        "Content-Type": "video/mp4",
    },
    method="PUT",
)
with urllib.request.urlopen(put_req) as resp:
    print("Upload status:", resp.status)

print(f"\nDone. publish_id = {publish_id}")
print("Check your TikTok app's inbox/drafts for the uploaded video.")
