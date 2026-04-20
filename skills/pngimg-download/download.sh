#!/bin/bash
# pngimg-download: Search and download PNG images from pngimg.com

set -euo pipefail

BASE_URL="https://pngimg.com"
ACTION="${1:-help}"
KEYWORD="${2:-}"
COUNT="${3:-1}"
OUTPUT_DIR="${4:-.}"

usage() {
  echo "Usage: bash download.sh <search|download> <keyword> [count] [output_dir]"
  echo ""
  echo "Commands:"
  echo "  search <keyword>                    List available PNG images"
  echo "  download <keyword> [count] [dir]    Download images (default: 1, current dir)"
  echo ""
  echo "Examples:"
  echo "  bash download.sh search cat"
  echo "  bash download.sh download apple 3 ./assets/"
  exit 0
}

# Extract full-size image URLs from search results
fetch_image_urls() {
  local keyword="$1"
  local url="${BASE_URL}/search_image/?search_image=${keyword}"
  # Get thumbnail paths, convert to full-size by removing 'small/'
  curl -sL "$url" \
    | grep -oE "uploads/[^\"' ]+\.png" \
    | sed 's|/small/|/|g' \
    | sort -u
}

search() {
  local keyword="$1"
  echo "Searching pngimg.com for: ${keyword}"
  echo ""

  local links
  links=$(fetch_image_urls "$keyword")

  if [ -z "$links" ]; then
    echo "No images found for '${keyword}'."
    echo "Try different keywords or check https://pngimg.com"
    exit 1
  fi

  local count=0
  while IFS= read -r link; do
    count=$((count + 1))
    echo "  [${count}] ${BASE_URL}/${link}"
  done <<< "$links"
  echo ""
  echo "Found ${count} images."
}

download() {
  local keyword="$1"
  local max="$2"
  local outdir="$3"

  mkdir -p "$outdir"
  echo "Downloading up to ${max} PNG images for '${keyword}' to ${outdir}/"

  local links
  links=$(fetch_image_urls "$keyword")

  if [ -z "$links" ]; then
    echo "No images found for '${keyword}'."
    exit 1
  fi

  local count=0
  while IFS= read -r link; do
    [ "$count" -ge "$max" ] && break
    count=$((count + 1))
    local filename
    filename=$(basename "$link")
    local url="${BASE_URL}/${link}"
    echo "  [${count}/${max}] Downloading ${filename}..."
    if curl -sfL -o "${outdir}/${filename}" "$url"; then
      echo "         Saved: ${outdir}/${filename}"
    else
      echo "         Failed to download, skipping."
      count=$((count - 1))
    fi
  done <<< "$links"

  echo ""
  echo "Done. Downloaded ${count} images to ${outdir}/"
}

case "$ACTION" in
  search)
    [ -z "$KEYWORD" ] && { echo "Error: keyword required"; usage; }
    search "$KEYWORD"
    ;;
  download)
    [ -z "$KEYWORD" ] && { echo "Error: keyword required"; usage; }
    download "$KEYWORD" "$COUNT" "$OUTPUT_DIR"
    ;;
  *)
    usage
    ;;
esac
