# SVG Output Format Reference

## When to Use

- User requests a `.svg` file
- User wants to import into vector editors (Figma, Illustrator, Sketch)
- User wants to embed SVG directly in documents
- User plans to use PNG/PDF export script

## How to Generate Standalone SVG

### Step 1: Generate the diagram JSON as normal

### Step 2: Output SVG instead of HTML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 WIDTH HEIGHT" xmlns="http://www.w3.org/2000/svg" width="WIDTH" height="HEIGHT">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap');
    text { font-family: 'JetBrains Mono', monospace; }
  </style>
  <defs><!-- patterns, markers, filters --></defs>
  <!-- diagram content -->
</svg>
```

### Rules

1. Start with `<?xml version="1.0" encoding="UTF-8"?>`
2. Add `xmlns="http://www.w3.org/2000/svg"` on root `<svg>`
3. All CSS in a `<style>` block inside the `<svg>` element
4. Fonts via `@import` inside SVG `<style>`, NOT external `<link>` tags
5. No HTML wrapper, no cards, no footer
6. No JavaScript
7. File extension: `.svg`

### Include/Exclude

| Element | Include? |
|---------|----------|
| Grid/background, components, connections, labels, legend, defs | Yes |
| Summary cards, page footer | No |
| Pulsing dot animation | Optional |

## Font Handling

**Online (default)**: Use `@import url(...)` in SVG `<style>`

**Offline fallback**: Use system font stack:
```css
text { font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace; }
```

## Limitations

- Google Fonts need network access
- Some viewers don't support CSS `@import`
- Filters (cyberpunk glow) may render differently
- For offline, embed fonts as base64 (advanced)
