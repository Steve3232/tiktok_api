#!/usr/bin/env python3
"""
Step 3 of the demo flow: upload a video to TikTok as a draft in the
creator's inbox, via the Content Posting API's inbox/draft flow
(push_by_file — direct upload, no domain verification needed).

Two different "init" endpoints exist and need different scopes — this
tripped us up once already, worth remembering:
  - /v2/post/publish/video/init/        -> Direct Post, needs `video.publish`
  - /v2/post/publish/inbox/video/init/  -> draft to inbox, needs `video.upload`
This script uses the inbox one, matching the `video.upload` scope granted
during OAuth. The inbox endpoint doesn't take post_info (title/privacy
etc.) — the creator sets that themselves when they open the draft in the
TikTok app and finish posting it.

Usage:
    python3 3_post_video.py /path/to/video.mp4
"""
import json
import os
import sys
import urllib.request

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")

if len(sys.argv) != 2:
    sys.exit("Usage: python3 3_post_video.py <video_path>")

video_path = sys.argv[1]

with open(TOKEN_PATH) as f:
    token_data = json.load(f)
access_token = token_data["access_token"]

video_size = os.path.getsize(video_path)

init_body = json.dumps({
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size,
        "chunk_size": video_size,
        "total_chunk_count": 1,
    },
}).encode()

req = urllib.request.Request(
    "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
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
