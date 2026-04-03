# MagicaVoxel Palette Usage

## Overview
This project uses an extracted palette from your MagicaVoxel palette image (`Pallet/pallet.png`). The palette contains 255 colors and is automatically used in all voxel creation scripts.

## Files Created

### 1. `magica_palette.json`
- Contains 255 extracted colors from your palette
- Format: `[[r, g, b, a], [r, g, b, a], ...]`
- Automatically loaded by all scripts

### 2. `palette_utils.py`
Utility functions for working with the palette:
- `get_palette()` - Get the full palette
- `get_color_by_index(index)` - Get color by index
- `find_closest_color_index(rgb)` - Find closest color index for RGB values

### 3. `extract_palette.py`
Script to extract colors from PNG palette files:
```bash
python extract_palette.py
```

### 4. `create_red_cube.py`
Example script that creates a red cube using the extracted palette:
```bash
python create_red_cube.py
```

## Usage Examples

### Basic Usage
```python
from palette_utils import get_palette, find_closest_color_index

# Get the full palette
palette = get_palette()

# Find red color index
red_index = find_closest_color_index([255, 0, 0])
red_color = palette[red_index]
print(f"Red color: {red_color}")
```

### Creating VOX Files with Custom Palette
```python
import pyvox.models
import pyvox.writer
from palette_utils import get_palette, find_closest_color_index

# Get your palette
palette = get_palette()

# Find color indices
red_index = find_closest_color_index([255, 0, 0])
blue_index = find_closest_color_index([0, 0, 255])

# Create voxels with custom colors
voxels = [
    pyvox.models.Voxel(0, 0, 0, red_index),
    pyvox.models.Voxel(1, 0, 0, blue_index),
]

# Create model with your palette
model = pyvox.models.Model((2, 1, 1), voxels)
vox = pyvox.models.Vox([model], palette=palette)

# Write file
writer = pyvox.writer.VoxWriter('output.vox', vox)
writer.write()
```

## Color Index Reference

Your palette contains 255 colors (indices 0-254):
- **Index 0**: Black [0, 0, 0, 255]
- **Index 1**: [0, 0, 17, 255]
- **Index 2**: [0, 0, 34, 255]
- ...
- **Index 88**: Pure Red [255, 0, 0, 255]
- ...
- **Index 254**: White [255, 255, 255, 255]

## Important Notes

1. **Always Use Your Palette**: All scripts automatically load `magica_palette.json`
2. **Fallback**: If palette file is missing, standard 8-color palette is used
3. **Color Matching**: Use `find_closest_color_index()` to find the best match for any RGB color
4. **Visualization**: Warning "_t in nTRN not match models, transform not applied" is normal and doesn't affect the result

## Updating Palette

To update the palette:
1. Replace `Pallet/pallet.png` with new palette image
2. Run: `python extract_palette.py`
3. New palette will be saved to `magica_palette.json`

## Dependencies

```bash
pip install pyvox midvoxio pillow numpy
```
