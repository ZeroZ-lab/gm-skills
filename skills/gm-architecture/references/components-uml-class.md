# UML Class Diagram — Component Templates

## Class Box

foreignObject + CSS, 3-section layout:

```svg
<g transform="translate(BOX_X, BOX_Y)">
  <!-- Background rect -->
  <rect width="BOX_W" height="BOX_H" rx="4"
        fill="FILL_COLOR" stroke="STROKE_COLOR" stroke-width="1"/>

  <!-- Header section -->
  <foreignObject width="BOX_W" height="HEADER_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="uml-header">
      <div class="uml-stereotype">&lt;&lt;interface&gt;&gt;</div>
      <div class="uml-class-name">ClassName</div>
    </div>
  </foreignObject>

  <!-- Divider 1 -->
  <line x1="0" y1="HEADER_H" x2="BOX_W" y2="HEADER_H"
        stroke="DIVIDER_COLOR" stroke-width="0.5"/>

  <!-- Attributes section -->
  <foreignObject y="HEADER_H" width="BOX_W" height="ATTRS_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="uml-section">
      <div class="uml-attr">- name : String</div>
      <div class="uml-attr"># age : int</div>
    </div>
  </foreignObject>

  <!-- Divider 2 -->
  <line x1="0" y1="DIVIDER2_Y" x2="BOX_W" y2="DIVIDER2_Y"
        stroke="DIVIDER_COLOR" stroke-width="0.5"/>

  <!-- Methods section -->
  <foreignObject y="DIVIDER2_Y" width="BOX_W" height="METHODS_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="uml-section">
      <div class="uml-method">+ getName() : String</div>
      <div class="uml-method">+ setName(name : String) : void</div>
    </div>
  </foreignObject>
</g>
```

CSS classes:
- `.uml-header`: Center-aligned, bold name
- `.uml-stereotype`: Italic, smaller font, centered
- `.uml-class-name`: Bold, centered
- `.uml-section`: Left-aligned, monospace
- `.uml-attr`: Left-aligned, padding 2px 12px
- `.uml-method`: Left-aligned, padding 2px 12px

## Relationship Lines

### Inheritance (solid + hollow triangle)

```svg
<defs>
  <marker id="inheritance" markerWidth="12" markerHeight="10" refX="12" refY="5" orient="auto">
    <polygon points="0,0 12,5 0,10" fill="white" stroke="STROKE_COLOR" stroke-width="1"/>
  </marker>
</defs>
<path d="..." fill="none" stroke="STROKE_COLOR" stroke-width="1.5"
      marker-end="url(#inheritance)"/>
```

### Implementation (dashed + hollow triangle)

Same as inheritance but with `stroke-dasharray="8 4"`.

### Composition (solid + filled diamond)

```svg
<marker id="composition" markerWidth="12" markerHeight="10" refX="0" refY="5" orient="auto">
  <polygon points="0,5 6,0 12,5 6,10" fill="STROKE_COLOR"/>
</marker>
<path d="..." fill="none" stroke="STROKE_COLOR" stroke-width="1.5"
      marker-start="url(#composition)"/>
```

Diamond on the "whole" side (the `from` class).

### Aggregation (solid + hollow diamond)

Same as composition but diamond `fill="white"`.

### Association (solid + open arrow)

```svg
<marker id="association" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
  <polyline points="0,0 8,3 0,6" fill="none" stroke="STROKE_COLOR" stroke-width="1.5"/>
</marker>
```

### Dependency (dashed + open arrow)

Same as association but with `stroke-dasharray="6 4"`.

## Multiplicity Label

```svg
<text x="LABEL_X" y="LABEL_Y"
      font-size="10" fill="TEXT_COLOR"
      text-anchor="start" dominant-baseline="central">
  1..*
</text>
```

Placed near the endpoint of the relationship, offset by 6px.
