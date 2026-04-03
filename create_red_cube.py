#!/usr/bin/env python3
"""
Create red cube using extracted MagicaVoxel palette
"""

import pyvox.models
import pyvox.writer
from midvoxio.voxio import viz_vox
from palette_utils import get_palette, find_closest_color_index

def create_red_cube(size=3):
    """Create red cube using extracted palette"""
    # Get the palette
    palette = get_palette()
    
    # Find red color index (or closest to red)
    red_index = find_closest_color_index([255, 0, 0])
    
    # Create voxels
    voxels = []
    for x in range(size):
        for y in range(size):
            for z in range(size):
                voxels.append(pyvox.models.Voxel(x, y, z, red_index))
    
    # Create model
    model = pyvox.models.Model((size, size, size), voxels)
    vox = pyvox.models.Vox([model], palette=palette)
    
    # Write file
    output_file = "red_cube.vox"
    writer = pyvox.writer.VoxWriter(output_file, vox)
    writer.write()
    
    print(f"Created red cube: {output_file}")
    print(f"Used palette with {len(palette)} colors")
    print(f"Red color index: {red_index}")
    print(f"Red color RGB: {palette[red_index]}")
    
    return output_file

if __name__ == "__main__":
    # Create and visualize red cube
    vox_file = create_red_cube(3)
    viz_vox(vox_file)
