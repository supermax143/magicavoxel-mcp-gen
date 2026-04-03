# MagicaVoxel MCP Generator

A comprehensive toolkit for working with MagicaVoxel files and palettes. This project provides utilities for extracting colors from palette images, creating voxel models, and working with custom palettes.

## Features

- 🎨 **Palette Extraction**: Extract colors from MagicaVoxel palette PNG files
- 🎯 **Color Matching**: Find closest color matches for any RGB value
- 📦 **VOX Creation**: Create voxel models using custom palettes
- 🖼️ **Visualization**: Preview voxel models with MidVoxIO
- 🔧 **Easy Integration**: Simple utilities for any voxel project

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/magicavoxel-mcp-gen.git
cd magicavoxel-mcp-gen
pip install -r requirements.txt
```

### Basic Usage

```python
from palette_utils import get_palette, find_closest_color_index
import pyvox.models
import pyvox.writer

# Get your custom palette
palette = get_palette()

# Find color indices
red_index = find_closest_color_index([255, 0, 0])
blue_index = find_closest_color_index([0, 0, 255])

# Create voxels
voxels = [
    pyvox.models.Voxel(0, 0, 0, red_index),
    pyvox.models.Voxel(1, 0, 0, blue_index),
]

# Create and save model
model = pyvox.models.Model((2, 1, 1), voxels)
vox = pyvox.models.Vox([model], palette=palette)
writer = pyvox.writer.VoxWriter('output.vox', vox)
writer.write()
```

## Project Structure

```
magicavoxel-mcp-gen/
├── Pallet/                 # Your palette images
│   └── pallet.png         # MagicaVoxel palette
├── palette_utils.py       # Core palette utilities
├── extract_palette.py     # Extract colors from PNG
├── create_red_cube.py     # Example usage
├── magica_palette.json    # Extracted palette data
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Available Scripts

### Extract Palette
Extract colors from a PNG palette file:
```bash
python extract_palette.py
```

### Create Red Cube
Create a red cube using your palette:
```bash
python create_red_cube.py
```

## Palette System

The project uses a 255-color palette extracted from your MagicaVoxel palette image. The palette is automatically loaded by all scripts and includes:

- **255 unique colors** with full RGBA values
- **Automatic color matching** for any RGB input
- **Fallback support** if palette file is missing
- **Easy updates** - just replace the PNG and re-run extraction

## API Reference

### palette_utils.py

```python
# Get the full palette
palette = get_palette()

# Get color by index
color = get_color_by_index(88)  # Returns [255, 0, 0, 255]

# Find closest color index for RGB values
red_index = find_closest_color_index([255, 0, 0])
```

## Examples

### Creating Custom Models
```python
import pyvox.models
import pyvox.writer
from palette_utils import get_palette, find_closest_color_index

# Create a gradient cube
def create_gradient_cube(size=5):
    palette = get_palette()
    voxels = []
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # Create color gradient
                r = int(255 * x / (size - 1))
                g = int(255 * y / (size - 1))
                b = int(255 * z / (size - 1))
                
                color_index = find_closest_color_index([r, g, b])
                voxels.append(pyvox.models.Voxel(x, y, z, color_index))
    
    model = pyvox.models.Model((size, size, size), voxels)
    vox = pyvox.models.Vox([model], palette=palette)
    
    writer = pyvox.writer.VoxWriter('gradient_cube.vox', vox)
    writer.write()
```

## Dependencies

- **pyvox**: For creating and writing VOX files
- **midvoxio**: For visualization and reading VOX files
- **Pillow**: For image processing
- **numpy**: For numerical operations
- **matplotlib**: For additional visualization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MagicaVoxel for the amazing voxel editor
- pyvox library for VOX file support
- MidVoxIO for visualization tools
