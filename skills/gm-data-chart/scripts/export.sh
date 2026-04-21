#!/usr/bin/env bash
# gmdiagram export script
# Converts HTML/SVG diagrams to PNG or PDF
#
# Usage: ./scripts/export.sh <input.html|input.svg> --format png|pdf [--output filename]
#
# Requirements:
#   PNG: Node.js + npm (uses @resvg/resvg-js)
#   PDF: rsvg-convert (brew install librsvg)

set -euo pipefail

INPUT=""
FORMAT=""
OUTPUT=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_SVG=""
TEMP_DIR=""
TEMP_PNG=""
PYTHON_BIN="${PYTHON_BIN:-python3}"

cleanup() {
  if [[ -n "${TEMP_SVG:-}" && -f "${TEMP_SVG:-}" ]]; then
    rm -f "$TEMP_SVG"
  fi
  if [[ -n "${TEMP_PNG:-}" && -f "${TEMP_PNG:-}" ]]; then
    rm -f "$TEMP_PNG"
  fi
  if [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR:-}" ]]; then
    rm -rf "$TEMP_DIR"
  fi
}

trap cleanup EXIT

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 <input.html|input.svg> --format png|pdf [--output filename]"
      echo ""
      echo "Formats:"
      echo "  png   Export as high-resolution PNG (2000px width) using @resvg/resvg-js"
      echo "  pdf   Export as vector PDF using rsvg-convert"
      echo ""
      echo "Requirements:"
      echo "  PNG: Node.js 18+ and npm"
      echo "  PDF: rsvg-convert (install via: brew install librsvg)"
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    *)
      INPUT="$1"
      shift
      ;;
  esac
done

# Validate
if [[ -z "$INPUT" ]]; then
  echo "Error: No input file specified" >&2
  echo "Usage: $0 <input.html|input.svg> --format png|pdf" >&2
  exit 1
fi

if [[ -z "$FORMAT" ]]; then
  echo "Error: No format specified. Use --format png or --format pdf" >&2
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Error: File not found: $INPUT" >&2
  exit 1
fi

# Validate format
if [[ "$FORMAT" != "png" && "$FORMAT" != "pdf" ]]; then
  echo "Error: Unknown format. Use 'png' or 'pdf'." >&2
  exit 1
fi

# Determine output filename
BASENAME="${INPUT%.*}"
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="${BASENAME}.${FORMAT}"
fi

# Validate output path is within current working directory
OUTPUT_REAL="$(cd "$(dirname "$OUTPUT")" 2>/dev/null && pwd)/$(basename "$OUTPUT")" || OUTPUT_REAL="$(pwd)/$OUTPUT"
ALLOWED_DIR="$(pwd)"
if [[ "$OUTPUT_REAL" != "$ALLOWED_DIR"* ]]; then
  echo "Error: Output file must be within current directory" >&2
  exit 1
fi

# Export based on format
case "$FORMAT" in
  png)
    # Check for Node.js
    if [[ "$INPUT" == *.html ]]; then
      echo "Extracting SVG from HTML..."
      TEMP_SVG="$(mktemp "${TMPDIR:-/tmp}/gmdiagram.XXXXXX")"
      chmod 600 "$TEMP_SVG"
      sed -n '/<svg/,/<\/svg>/p' "$INPUT" > "$TEMP_SVG"
      SVG_FILE="$TEMP_SVG"
    else
      SVG_FILE="$INPUT"
    fi

    # Extract background color from SVG or use white as default
    BG_COLOR=$(grep -o 'background[^;]*#\([0-9a-fA-F]\{3,8\}\)' "$SVG_FILE" | head -1 | grep -o '#[0-9a-fA-F]\{3,8\}' || echo "#ffffff")

    if command -v node &> /dev/null; then
      cd "$SCRIPT_DIR"
      if [[ ! -d "node_modules/@resvg/resvg-js" ]]; then
        echo "Installing @resvg/resvg-js..."
        npm install 2>&1 || {
          echo "Error: Failed to install @resvg/resvg-js" >&2
          exit 1
        }
      fi

      echo "Converting to PNG with resvg-js (2000px width)..."
      node -e "
        const { Resvg } = require('@resvg/resvg-js');
        const fs = require('fs');
        const svg = fs.readFileSync(process.argv[1]);
        const resvg = new Resvg(svg, {
          background: process.argv[3],
          fitTo: { mode: 'width', value: 2000 },
          font: { loadSystemFonts: true, defaultFontFamily: 'JetBrains Mono' }
        });
        const pngData = resvg.render();
        fs.writeFileSync(process.argv[2], pngData.asPng());
        console.log('Done: ' + process.argv[2] + ' (' + Math.round(pngData.asPng().length / 1024) + ' KB)');
      " "$SVG_FILE" "$OUTPUT" "$BG_COLOR"
    elif command -v "$PYTHON_BIN" &> /dev/null && "$PYTHON_BIN" -c "import cairosvg" &> /dev/null; then
      echo "Converting to PNG with CairoSVG (2000px width fallback)..."
      "$PYTHON_BIN" - <<'PY' "$SVG_FILE" "$OUTPUT" "$BG_COLOR"
import sys
import cairosvg

svg_path, out_path, bg = sys.argv[1], sys.argv[2], sys.argv[3]
cairosvg.svg2png(url=svg_path, write_to=out_path, output_width=2000, background_color=bg)
print(f"Done: {out_path}")
PY
    elif command -v qlmanage &> /dev/null; then
      echo "Converting to PNG with Quick Look fallback..."
      TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/gmdiagram-export.XXXXXX")"
      qlmanage -t -s 2000 -o "$TEMP_DIR" "$INPUT" >/dev/null
      THUMBNAIL="$(find "$TEMP_DIR" -maxdepth 1 -type f -name '*.png' | head -1)"
      if [[ -z "$THUMBNAIL" || ! -f "$THUMBNAIL" ]]; then
        echo "Error: Quick Look did not produce a PNG thumbnail" >&2
        exit 1
      fi
      mv "$THUMBNAIL" "$OUTPUT"
      echo "Done: $OUTPUT"
    else
      echo "Error: PNG export requires Node.js, python3 with cairosvg, or macOS Quick Look" >&2
      echo "Install Node.js from: https://nodejs.org" >&2
      echo "Or run: python3 -m pip install --user cairosvg" >&2
      exit 1
    fi
    ;;

  pdf)
    if [[ "$INPUT" == *.html ]]; then
      echo "Extracting SVG from HTML..."
      TEMP_SVG="$(mktemp "${TMPDIR:-/tmp}/gmdiagram.XXXXXX")"
      chmod 600 "$TEMP_SVG"
      sed -n '/<svg/,/<\/svg>/p' "$INPUT" > "$TEMP_SVG"
      SVG_FILE="$TEMP_SVG"
    else
      SVG_FILE="$INPUT"
    fi

    if command -v rsvg-convert &> /dev/null; then
      echo "Converting to vector PDF with rsvg-convert..."
      rsvg-convert -f pdf -o "$OUTPUT" "$SVG_FILE"
      echo "Done: $OUTPUT"
    elif command -v "$PYTHON_BIN" &> /dev/null && "$PYTHON_BIN" -c "import cairosvg" &> /dev/null; then
      echo "Converting to PDF with CairoSVG fallback..."
      "$PYTHON_BIN" - <<'PY' "$SVG_FILE" "$OUTPUT"
import sys
import cairosvg

svg_path, out_path = sys.argv[1], sys.argv[2]
cairosvg.svg2pdf(url=svg_path, write_to=out_path)
print(f"Done: {out_path}")
PY
    elif command -v qlmanage &> /dev/null && command -v sips &> /dev/null; then
      echo "Converting to PDF with Quick Look + sips fallback..."
      TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/gmdiagram-export.XXXXXX")"
      qlmanage -t -s 2000 -o "$TEMP_DIR" "$INPUT" >/dev/null
      TEMP_PNG="$(find "$TEMP_DIR" -maxdepth 1 -type f -name '*.png' | head -1)"
      if [[ -z "$TEMP_PNG" || ! -f "$TEMP_PNG" ]]; then
        echo "Error: Quick Look did not produce an intermediate PNG thumbnail" >&2
        exit 1
      fi
      sips -s format pdf "$TEMP_PNG" --out "$OUTPUT" >/dev/null
      echo "Done: $OUTPUT"
    else
      echo "Error: PDF export requires rsvg-convert, python3 with cairosvg, or macOS Quick Look + sips" >&2
      echo "Install librsvg via: brew install librsvg" >&2
      echo "Or run: python3 -m pip install --user cairosvg" >&2
      exit 1
    fi
    ;;

  *)
    echo "Error: Unknown format '$FORMAT'. Use 'png' or 'pdf'." >&2
    exit 1
    ;;
esac
