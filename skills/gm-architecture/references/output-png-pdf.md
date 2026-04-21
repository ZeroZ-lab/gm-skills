# PNG/PDF Export Reference

## Usage

After generating an HTML or SVG diagram, use the export script to convert:

```bash
# PNG export (high-resolution, 2000px width)
./scripts/export.sh diagram.html --format png

# PDF export (vector quality)
./scripts/export.sh diagram.html --format pdf

# SVG input also works
./scripts/export.sh diagram.svg --format png --output my-diagram.png
```

## Requirements

### PNG Export
- Preferred: **Node.js** 18+ (for `@resvg/resvg-js`)
- Fallback on macOS: **Quick Look** via `qlmanage`
- Optional fallback: **python3 + cairosvg** if system Cairo libraries are available

### PDF Export
- Preferred: **rsvg-convert** (from librsvg)
- Fallback on macOS: **Quick Look + sips**
- Optional fallback: **python3 + cairosvg** if system Cairo libraries are available
- Install librsvg: `brew install librsvg` (macOS) or `apt install librsvg2-bin` (Linux)

## How It Works

1. If input is HTML, extract the `<svg>` element using sed
2. For PNG:
   - prefer `@resvg/resvg-js` when Node.js is available
   - otherwise use macOS Quick Look thumbnail generation
   - otherwise try CairoSVG if available
3. For PDF:
   - prefer `rsvg-convert` for direct SVG-to-PDF conversion
   - otherwise use macOS Quick Look thumbnail generation plus `sips`
   - otherwise try CairoSVG if available

## Limitations

- PNG background defaults to `#020617` (dark) — adjust in the script for light styles
- Google Fonts need to be available on the system for accurate rendering in PNG
- SVG filters (cyberpunk glow) may render slightly differently in PNG vs browser
- Quick Look fallback generates raster previews; PDF output from the Quick Look path is image-based rather than vector-perfect
- CairoSVG requires system Cairo libraries; `pip install cairosvg` alone may not be sufficient on every machine
