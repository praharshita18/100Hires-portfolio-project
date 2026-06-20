#!/usr/bin/env bash
# Download YouTube transcripts for B2B SaaS content strategy experts
# Uses yt-dlp auto-generated captions (no API key required)

export PATH="$PATH:/Users/Praharshita/Library/Python/3.9/bin"
BASE="$(dirname "$0")/youtube-transcripts"

download_transcript() {
    local video_id="$1"
    local author_slug="$2"
    local out_dir="$BASE/$author_slug"
    local out_base="$out_dir/$video_id"
    local txt_file="$out_base.txt"

    mkdir -p "$out_dir"

    if [ -f "$txt_file" ]; then
        echo "  [SKIP] Already exists: $video_id"
        return
    fi

    echo "  [GET] $video_id -> $author_slug"

    # Download auto-captions only (no video)
    yt-dlp \
        --write-auto-sub \
        --skip-download \
        --sub-lang "en" \
        --sub-format "vtt" \
        --output "$out_base.%(ext)s" \
        --no-warnings \
        "https://www.youtube.com/watch?v=$video_id" 2>/dev/null

    # Find VTT file
    vtt_file=$(ls "$out_dir/${video_id}"*.vtt 2>/dev/null | head -1)

    if [ -z "$vtt_file" ]; then
        echo "  [WARN] No captions: $video_id"
        # Fetch title for placeholder
        title=$(yt-dlp --print "%(title)s" --no-warnings "https://www.youtube.com/watch?v=$video_id" 2>/dev/null)
        echo "# ${title:-$video_id}

URL: https://www.youtube.com/watch?v=$video_id
Collected: 2026-06-20

---

No auto-generated captions available for this video. Consider manual transcription or an alternative video source." > "$txt_file"
        return
    fi

    # Get title
    title=$(yt-dlp --print "%(title)s" --no-warnings "https://www.youtube.com/watch?v=$video_id" 2>/dev/null)

    # Convert VTT to clean text (strip timestamps, deduplicate)
    python3 - "$vtt_file" "$txt_file" "$title" "$video_id" <<'PYEOF'
import sys, re

vtt_path, out_path, title, vid_id = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

with open(vtt_path, encoding="utf-8", errors="ignore") as f:
    text = f.read()

lines = text.split("\n")
seen = set()
clean = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith(("WEBVTT", "Kind:", "Language:")):
        continue
    if re.match(r"^\d{2}:\d{2}:\d{2}", line):
        continue
    line = re.sub(r"<[^>]+>", "", line).strip()
    if not line or line in seen:
        continue
    seen.add(line)
    clean.append(line)

prose = " ".join(clean)

with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# {title}\n\n")
    f.write(f"URL: https://www.youtube.com/watch?v={vid_id}\n")
    f.write(f"Collected: 2026-06-20\n\n")
    f.write("---\n\n")
    f.write(prose)
    f.write("\n")

print(f"  [SAVED] {len(prose)} chars")
PYEOF

    rm -f "$vtt_file"
}

echo "=== Dave Gerhardt ==="
download_transcript "r9Kgv3OYlP0" "dave-gerhardt"
download_transcript "CPlZXWFc7G8" "dave-gerhardt"
download_transcript "i9YbJUDAwcg" "dave-gerhardt"
download_transcript "H4LpPMR6v1E" "dave-gerhardt"
download_transcript "I4VWFOcbr2s" "dave-gerhardt"

echo "=== Amanda Natividad ==="
download_transcript "PR3dYYau4T8" "amanda-natividad"
download_transcript "JZ0jue2ef9I" "amanda-natividad"
download_transcript "rLW2_ovhTag" "amanda-natividad"

echo "=== Anthony Pierri (Fletch PMM) ==="
download_transcript "gu8WMjFe_cU" "anthony-pierri"
download_transcript "xjrpOsixMrA" "anthony-pierri"

echo "=== Chris Walker ==="
download_transcript "ZIRoWKZbG-M" "chris-walker"
download_transcript "h6aBRrKHAAA" "chris-walker"
download_transcript "RBQsTE6glec" "chris-walker"

echo "=== Gaetano DiNardi ==="
download_transcript "MAQdQvEui6s" "gaetano-dinardi"
download_transcript "_gNHaVp0ikc" "gaetano-dinardi"

echo "=== Tommy Clark ==="
download_transcript "vcFh5-fynHc" "tommy-clark"
download_transcript "5lcZl4iEjI0" "tommy-clark"
download_transcript "K2H2KGTbZ08" "tommy-clark"
download_transcript "BMfXeo02bvo" "tommy-clark"

echo "=== Alex Lieberman ==="
download_transcript "Z2pV8F9B9JM" "alex-lieberman"
download_transcript "HNAgxVeyNhk" "alex-lieberman"
download_transcript "wW9wv0zSMKU" "alex-lieberman"

echo "=== Maja Voje ==="
download_transcript "MKdCh1dBHNk" "maja-voje"
download_transcript "fCF2WlcNx3Q" "maja-voje"
download_transcript "3pfSupyJ2bo" "maja-voje"
download_transcript "KSQwuJUB3sw" "maja-voje"

echo "=== Kyle Poyar ==="
download_transcript "bz4BB2d5sSE" "kyle-poyar"
download_transcript "EwaQiW216J4" "kyle-poyar"
download_transcript "KPajt_mhHG8" "kyle-poyar"
download_transcript "aYX1x3Vmr-0" "kyle-poyar"

echo ""
echo "All transcripts downloaded."
