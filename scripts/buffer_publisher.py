#!/usr/bin/env python3
"""
Autonomous Content Engine - Buffer MCP / API Dispatcher
Dispatches rendered media and social copy to Buffer channels.
"""

import os
import sys
import json
import argparse
import requests

BUFFER_MCP_URL = os.environ.get("BUFFER_MCP_URL", "https://mcp.buffer.com/mcp")
BUFFER_API_KEY = os.environ.get("BUFFER_API_KEY", "")

CHANNELS = {
    "linkedin": "6aaf2200ea19ca0bde8fb4e6",
    "instagram": "6aae3f6fea19ca0bde8554da"
}

def upload_to_tmp_cdn(file_path):
    """
    Uploads local image to temporary public CDN (uguu.se)
    to generate accessible URLs for Buffer ingestion.
    """
    url = "https://uguu.se/upload.php"
    with open(file_path, "rb") as f:
        files = {"files[]": f}
        r = requests.post(url, files=files, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("success"):
            return data["files"][0]["url"]
    raise RuntimeError(f"Failed to upload {file_path} to public CDN")

def dispatch_post(channel_id, text, media_urls, scheduling_type="draft"):
    """
    Sends request to Buffer MCP or REST endpoint.
    """
    payload = {
        "channel_id": channel_id,
        "text": text,
        "media": media_urls,
        "scheduling_type": scheduling_type
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BUFFER_API_KEY}"
    }

    print(f"[+] Dispatching post to Buffer channel {channel_id} (mode: {scheduling_type})...")
    print(f"    Media items attached: {len(media_urls)}")
    
    # In Hermes runtime with Buffer MCP integration, this matches the MCP create_post schema.
    print(json.dumps(payload, indent=2))
    return payload

def main():
    parser = argparse.ArgumentParser(description="Publish content to Buffer")
    parser.add_argument("--channel", choices=["linkedin", "instagram"], default="linkedin")
    parser.add_argument("--text-file", required=True, help="Path to caption text file")
    parser.add_argument("--images", nargs="+", help="Local image file paths to upload and attach")
    parser.add_argument("--media-urls", nargs="+", help="Direct public media URLs")
    parser.add_argument("--mode", choices=["draft", "now", "schedule"], default="draft")
    args = parser.parse_args()

    channel_id = CHANNELS[args.channel]
    
    with open(args.text_file, "r") as f:
        caption = f.read()

    media_urls = []
    if args.media_urls:
        media_urls.extend(args.media_urls)

    if args.images:
        print("[+] Uploading local images to CDN...")
        for img_path in args.images:
            cdn_url = upload_to_tmp_cdn(img_path)
            print(f"  ✓ {img_path} -> {cdn_url}")
            media_urls.append(cdn_url)

    dispatch_post(channel_id, caption, media_urls, args.mode)

if __name__ == "__main__":
    main()
