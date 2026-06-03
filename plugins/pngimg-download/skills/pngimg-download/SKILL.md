---
name: pngimg-download
description: "Search and download free transparent PNG images from pngimg.com. Use when the user wants to find or download PNG images with transparent backgrounds, clipart, or icons for design projects."
allowed-tools: Bash(bash *download.sh*)
---

# pngimg-download

Search and download free transparent PNG images from [pngimg.com](https://pngimg.com/).

## How It Works

pngimg.com organizes images by category. The script uses the search API:
- Search endpoint: `https://pngimg.com/search_image/?search_image={keyword}`
- Result images are extracted from `/uploads/...` paths on the search results page

## Usage

### Search for images

Browse a category page to find available images:

```bash
bash "$(dirname "$0")/download.sh" search <keyword>
```

This fetches the category page and lists available PNG images with their download URLs.

### Download images

Download a specific image or multiple images from a category:

```bash
# Download first N images from a category
bash "$(dirname "$0")/download.sh" download <keyword> [count] [output_dir]
```

Parameters:
- `keyword` (required): The image category to search (e.g., cat, apple, car)
- `count` (optional): Number of images to download (default: 1)
- `output_dir` (optional): Output directory (default: current directory)

## Examples

```bash
# Search for cat images
bash "$(dirname "$0")/download.sh" search cat

# Download 3 cat images to current directory
bash "$(dirname "$0")/download.sh" download cat 3

# Download 5 apple images to ./assets/
bash "$(dirname "$0")/download.sh" download apple 5 ./assets/
```

## Notes

- All images have transparent backgrounds (PNG with alpha)
- License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
- Keywords are case-insensitive and use the category name from pngimg.com
- Some categories use compound names (e.g., "palm_tree", "ice_cream")
