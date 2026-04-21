# UML Class Diagram — Layout Rules

## Overall Structure

```
┌──────────────┐          ┌──────────────┐
│  <<interface>>│          │   Animal     │
│   IShape     │          │──────────────│
│──────────────│◄─────────│- name: String│
│+ draw(): void│          │- age: int    │
│+ area(): float│          │──────────────│
└──────────────┘          │+ makeSound() │
                          └──────────────┘
                                ▲
                                │
                          ┌──────────────┐
                          │     Dog      │
                          │──────────────│
                          │+ fetch(): void│
                          └──────────────┘
```

## Class Box Layout

### 3-Section Layout

Each class box has 3 horizontal sections:
1. **Header**: Class name + optional stereotype
2. **Attributes**: List of fields
3. **Methods**: List of methods

### Auto-sizing

- Box width = `max(header_width, max_attr_width, max_method_width) + 2 * PADDING`
- Header height: `28px` (or `38px` with stereotype)
- Attribute row height: `20px` per attribute
- Method row height: `20px` per method
- Minimum box width: `120px`
- Padding: `12px` horizontal, `6px` vertical

### Section Dividers

Thin horizontal lines between sections:
```svg
<line x1="0" y1="SECTION_Y" x2="BOX_W" y2="SECTION_Y" stroke="DIVIDER_COLOR" stroke-width="0.5"/>
```

## Visibility Markers

| Symbol | Visibility | Display |
|--------|-----------|---------|
| `+` | Public | `+ name: Type` |
| `-` | Private | `- name: Type` |
| `#` | Protected | `# name: Type` |
| `~` | Package | `~ name: Type` |

## Stereotype Display

Shown above class name in guillemets:
```
<<interface>>
  IShape
```

Use italic font for abstract classes.

## Spacing

- Minimum gap between classes: `40px`
- Relationship line offset from box edge: `8px`
- Multiplicity label offset: `6px` from endpoint

## Relationship Routing

Orthogonal routing (horizontal + vertical segments only):
1. Start from the appropriate edge of the source class
2. Route horizontally to clear the class boundary
3. Route vertically to the target class's edge level
4. Route horizontally to the target class

Avoid crossing through other class boxes.

## Density Multipliers

| Property | Compact | Normal | Spacious |
|----------|---------|--------|----------|
| Row height | 16px | 20px | 24px |
| Padding | 8px | 12px | 16px |
| Gap between classes | 30px | 40px | 60px |
| Font size | 10px | 12px | 13px |
| Header height | 24px | 28px | 34px |

## ViewBox

- Width: `max(class_positions) + max(class_widths) + 60`
- Height: `max(class_positions) + max(class_heights) + 60`
