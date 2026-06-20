#!/usr/bin/env python3
"""
Fetch YouTube transcripts using youtube-transcript-api.
No API key required — uses YouTube's built-in transcript endpoint.
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

from youtube_transcript_api import YouTubeTranscriptApi

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube-transcripts")

VIDEOS = [
    # Dave Gerhardt
    ("dave-gerhardt", "r9Kgv3OYlP0", "How to Master LinkedIn for B2B"),
    ("dave-gerhardt", "CPlZXWFc7G8", "The B2B content flywheel playbook"),
    ("dave-gerhardt", "i9YbJUDAwcg", "B2B Content Strategy: AI, SEO, and What's Working on LinkedIn and X"),
    ("dave-gerhardt", "H4LpPMR6v1E", "Founder Brand Creation with Dave Gerhardt"),
    ("dave-gerhardt", "I4VWFOcbr2s", "AI Idea Starters, B2B Influencers, & Organic LinkedIn Tactics"),
    # Amanda Natividad
    ("amanda-natividad", "PR3dYYau4T8", "Public Speaking is the Ultimate Zero-Click Marketing"),
    ("amanda-natividad", "JZ0jue2ef9I", "Amanda Natividad Shares How to Get Started with Zero-Click Content"),
    ("amanda-natividad", "rLW2_ovhTag", "The Art of Zero-Click Content"),
    # Anthony Pierri
    ("anthony-pierri", "gu8WMjFe_cU", "How to position your product"),
    ("anthony-pierri", "xjrpOsixMrA", "Ranking YCombinator Homepages"),
    # Chris Walker
    ("chris-walker", "ZIRoWKZbG-M", "Building Refine Labs - Demand Gen LIVE!"),
    ("chris-walker", "h6aBRrKHAAA", "3 Questions You'll Need To Know As a Refine Labs Director of Demand Gen"),
    ("chris-walker", "RBQsTE6glec", "First 90 Days as Head of Marketing - Chris Walker"),
    # Gaetano DiNardi
    ("gaetano-dinardi", "MAQdQvEui6s", "Brand Impact on Organic Search with Gaetano DiNardi"),
    ("gaetano-dinardi", "_gNHaVp0ikc", "How Saleshacker Grew 426% & Used SEO To Get Acquired - Gaetano DiNardi"),
    # Tommy Clark
    ("tommy-clark", "vcFh5-fynHc", "The Only LinkedIn Content Strategy You Need in 2025"),
    ("tommy-clark", "5lcZl4iEjI0", "The Best LinkedIn Content Strategy for SaaS"),
    ("tommy-clark", "K2H2KGTbZ08", "The Best LinkedIn Content Strategy for 2025"),
    ("tommy-clark", "BMfXeo02bvo", "The NEW Rules of LinkedIn (2026)"),
    # Alex Lieberman
    ("alex-lieberman", "Z2pV8F9B9JM", "Morning Brew's Co-founders Share Secrets Behind $75 Million Success"),
    ("alex-lieberman", "HNAgxVeyNhk", "Top 3 Priorities When Starting A New Business"),
    ("alex-lieberman", "wW9wv0zSMKU", "How Morning Brew's Alex Lieberman Went From Zero to $75 Million"),
    # Maja Voje
    ("maja-voje", "MKdCh1dBHNk", "How is AI Transforming Go To Market for B2B SaaS with Maja Voje"),
    ("maja-voje", "fCF2WlcNx3Q", "The Go-To-Market Strategist: Maja Voje on Winning GTM Strategies"),
    ("maja-voje", "3pfSupyJ2bo", "How to master the Go-To-Market strategy - Maja Voje"),
    ("maja-voje", "KSQwuJUB3sw", "The ultimate playbook to master Go-To-Market strategy - Maja Voje"),
    # Kyle Poyar
    ("kyle-poyar", "bz4BB2d5sSE", "Pricing for Product Led Growth - Kyle Poyar"),
    ("kyle-poyar", "EwaQiW216J4", "Product-Led Growth Through Usage Based Pricing by Kyle Poyar"),
    ("kyle-poyar", "KPajt_mhHG8", "The price is right: how to package for growth with Kyle Poyar"),
    ("kyle-poyar", "aYX1x3Vmr-0", "Unlocking Growth: Product-Led Growth meets Partnerships with Kyle Poyar"),
]

api = YouTubeTranscriptApi()
ok, skip, fail = 0, 0, 0

for (slug, vid_id, title) in VIDEOS:
    out_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip().replace(" ", "_")[:60]
    out_path = os.path.join(out_dir, f"{vid_id}_{safe_title}.txt")

    if os.path.exists(out_path):
        print(f"[SKIP] {slug}/{vid_id}")
        skip += 1
        continue

    try:
        transcript = api.fetch(vid_id)
        text = " ".join(s.text for s in transcript)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"URL: https://www.youtube.com/watch?v={vid_id}\n")
            f.write(f"Collected: 2026-06-20\n\n")
            f.write("---\n\n")
            f.write(text)
            f.write("\n")
        print(f"[OK]   {slug}/{vid_id} — {len(text)} chars")
        ok += 1
    except Exception as e:
        # Write placeholder
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"URL: https://www.youtube.com/watch?v={vid_id}\n")
            f.write(f"Collected: 2026-06-20\n\n")
            f.write("---\n\n")
            f.write(f"Transcript unavailable: {e}\n")
        print(f"[FAIL] {slug}/{vid_id} — {e}")
        fail += 1

print(f"\nDone. {ok} fetched, {skip} skipped, {fail} failed.")
