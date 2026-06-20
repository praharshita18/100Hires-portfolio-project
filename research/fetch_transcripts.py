#!/usr/bin/env python3
"""
Fetch YouTube transcripts for B2B SaaS content strategy experts.
Uses yt-dlp to download auto-generated captions (no API key required).
Outputs plain-text transcripts organized by author.
"""

import subprocess
import os
import sys
import json
import re

EXPERTS = [
    {
        "slug": "dave-gerhardt",
        "name": "Dave Gerhardt",
        "channel_url": "https://www.youtube.com/@exitfivedave",
        "max_videos": 5,
    },
    {
        "slug": "amanda-natividad",
        "name": "Amanda Natividad",
        "channel_url": "https://www.youtube.com/@sparktoro",
        "max_videos": 5,
    },
    {
        "slug": "anthony-pierri",
        "name": "Anthony Pierri",
        "channel_url": "https://www.youtube.com/@fletchpmm",
        "max_videos": 5,
    },
    {
        "slug": "chris-walker",
        "name": "Chris Walker",
        "channel_url": "https://www.youtube.com/@refinelabs",
        "max_videos": 5,
    },
    {
        "slug": "gaetano-dinardi",
        "name": "Gaetano DiNardi",
        "channel_url": "https://www.youtube.com/@gaetanodinardi",
        "max_videos": 5,
    },
    {
        "slug": "tommy-clark",
        "name": "Tommy Clark",
        "channel_url": "https://www.youtube.com/@tommyclarkk",
        "max_videos": 5,
    },
    {
        "slug": "alex-lieberman",
        "name": "Alex Lieberman",
        "channel_url": "https://www.youtube.com/@AlexLiebermanYT",
        "max_videos": 5,
    },
    {
        "slug": "maja-voje",
        "name": "Maja Voje",
        "channel_url": "https://www.youtube.com/@MajaVoje",
        "max_videos": 5,
    },
    {
        "slug": "kyle-poyar",
        "name": "Kyle Poyar",
        "channel_url": "https://www.youtube.com/@openviewpartners",
        "max_videos": 5,
    },
]

BASE_DIR = os.path.join(os.path.dirname(__file__), "youtube-transcripts")


def clean_vtt(vtt_text):
    """Strip VTT timestamps and deduplicate lines into clean prose."""
    lines = vtt_text.split("\n")
    seen = set()
    clean = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        # Skip timestamp lines like 00:00:01.000 --> 00:00:04.000
        if re.match(r"^\d{2}:\d{2}:\d{2}", line):
            continue
        # Strip inline VTT tags like <00:00:01.234><c>
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line:
            continue
        if line not in seen:
            seen.add(line)
            clean.append(line)
    return " ".join(clean)


def fetch_expert(expert):
    slug = expert["slug"]
    name = expert["name"]
    channel_url = expert["channel_url"]
    max_videos = expert["max_videos"]
    out_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Fetching: {name}")
    print(f"Channel:  {channel_url}")
    print(f"{'='*60}")

    # Step 1: Get list of recent video URLs (flat playlist)
    list_cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-end", str(max_videos),
        "--print", "%(id)s\t%(title)s\t%(url)s",
        "--no-warnings",
        channel_url,
    ]
    try:
        result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=60)
        lines = [l for l in result.stdout.strip().split("\n") if l]
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT listing videos for {name}")
        return
    except Exception as e:
        print(f"  ERROR listing videos: {e}")
        return

    if not lines:
        print(f"  No videos found for {name}")
        return

    videos = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 2:
            vid_id = parts[0]
            title = parts[1]
            url = parts[2] if len(parts) > 2 else f"https://www.youtube.com/watch?v={vid_id}"
            videos.append({"id": vid_id, "title": title, "url": url})

    print(f"  Found {len(videos)} videos")

    # Step 2: Download auto-captions for each video
    for i, video in enumerate(videos[:max_videos], 1):
        vid_id = video["id"]
        title = video["title"]
        url = video["url"]

        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:60]
        out_base = os.path.join(out_dir, f"{i:02d}_{safe_title}")
        vtt_path = f"{out_base}.en.vtt"
        txt_path = f"{out_base}.txt"

        if os.path.exists(txt_path):
            print(f"  [{i}] Already exists: {safe_title[:40]}")
            continue

        print(f"  [{i}] Downloading captions: {title[:50]}")

        caption_cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--skip-download",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--output", out_base + ".%(ext)s",
            "--no-warnings",
            url,
        ]
        try:
            subprocess.run(caption_cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT downloading captions")
            continue

        # Find the downloaded VTT file (yt-dlp names it slightly differently)
        vtt_files = [f for f in os.listdir(out_dir) if f.startswith(f"{i:02d}_") and f.endswith(".vtt")]
        if not vtt_files:
            print(f"    No captions available (video may lack auto-captions)")
            # Write a placeholder
            with open(txt_path, "w") as f:
                f.write(f"# {title}\n\nURL: {url}\n\nNo auto-generated captions available for this video.\n")
            continue

        # Convert VTT to clean text
        vtt_file = os.path.join(out_dir, vtt_files[0])
        with open(vtt_file, "r", encoding="utf-8", errors="ignore") as f:
            vtt_content = f.read()

        clean_text = clean_vtt(vtt_content)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"URL: {url}\n")
            f.write(f"Channel: {channel_url}\n")
            f.write(f"Collected: 2026-06-20\n\n")
            f.write("---\n\n")
            f.write(clean_text)
            f.write("\n")

        # Remove VTT file
        os.remove(vtt_file)
        print(f"    Saved transcript ({len(clean_text)} chars)")

    print(f"  Done: {name}")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    for expert in EXPERTS:
        if target and expert["slug"] != target:
            continue
        fetch_expert(expert)
    print("\n\nAll done!")


if __name__ == "__main__":
    main()
