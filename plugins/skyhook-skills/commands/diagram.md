Create an Excalidraw diagram and export it to PNG.

## Your task

Based on the user's description, create a diagram as a `.excalidraw` JSON file and export it to PNG using:

```bash
npx excalidraw-export-cli <input.excalidraw> [output.png]
```

If Playwright's Chromium isn't installed, run: `npx playwright install chromium`

## Excalidraw JSON format

The file must be valid JSON with this structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

## Element types

### Rectangle
```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 50, "y": 50,
  "width": 140, "height": 70,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#228be6",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "roundness": { "type": 3 },
  "seed": 1234
}
```

### Text
```json
{
  "id": "unique-id",
  "type": "text",
  "x": 65, "y": 75,
  "width": 110, "height": 20,
  "text": "Label",
  "fontSize": 14,
  "fontFamily": 5,
  "textAlign": "center",
  "strokeColor": "#ffffff",
  "seed": 1235
}
```

### Arrow
```json
{
  "id": "unique-id",
  "type": "arrow",
  "x": 195, "y": 85,
  "width": 80, "height": 0,
  "strokeColor": "#495057",
  "strokeWidth": 2,
  "roughness": 1,
  "points": [[0, 0], [80, 0]],
  "seed": 2234
}
```

### Ellipse
```json
{
  "id": "unique-id",
  "type": "ellipse",
  "x": 50, "y": 50,
  "width": 100, "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "seed": 3234
}
```

### Diamond
```json
{
  "id": "unique-id",
  "type": "diamond",
  "x": 50, "y": 50,
  "width": 100, "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#b2f2bb",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "seed": 4234
}
```

### Line
```json
{
  "id": "unique-id",
  "type": "line",
  "x": 50, "y": 50,
  "width": 200, "height": 0,
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "roughness": 1,
  "points": [[0, 0], [200, 0]],
  "seed": 5234
}
```

## Embedded images

To embed SVG or raster images (e.g., logos), add an `image` element and a corresponding entry in the `files` object:

```json
// In elements array:
{
  "id": "logo-img",
  "type": "image",
  "x": 102, "y": 118,
  "width": 36, "height": 35,
  "fileId": "logo-file-id",
  "status": "saved",
  "scale": [1, 1],
  "backgroundColor": "transparent",
  "seed": 99001
}

// In files object:
{
  "logo-file-id": {
    "mimeType": "image/svg+xml",
    "id": "logo-file-id",
    "dataURL": "data:image/svg+xml;base64,BASE64_ENCODED_SVG_HERE"
  }
}
```

Use official brand SVGs when available (e.g., Kubernetes logo from GitHub). Custom SVGs are fine when no official asset exists.

## Layout guidelines

- Space boxes 40-60px apart horizontally in flow diagrams
- Keep boxes at the same level aligned on the same y-position
- Place labels for arrows slightly above the arrow (y - 25)
- Use consistent box sizes for elements at the same level (e.g., all service boxes same width/height)
- Section labels go above their group, in a larger fontSize (18-20)
- Use `fontFamily: 5` (Excalifont/handwriting style) for all text
- Set unique `seed` values for every element (used for Excalidraw's hand-drawn randomization)

## Color palette

- Primary/accent boxes: `#228be6` (blue)
- External/infrastructure: `#495057` (dark gray)
- Success/positive: `#2f9e44` or `#b2f2bb`
- Warning: `#f08c00` or `#ffec99`
- Error/danger: `#e03131` or `#ffc9c9`
- Neutral background: `#dee2e6`
- White text on dark backgrounds: `#ffffff`
- Dark text/arrows: `#1e1e1e` or `#495057`
- Background: `#ffffff`

## Process

1. Design the diagram layout based on the user's description
2. Write the `.excalidraw` JSON file
3. Export to PNG: `npx excalidraw-export-cli <file.excalidraw> <output.png>`
4. Show the user the exported PNG

Ask the user where to save the files if not obvious from context.
