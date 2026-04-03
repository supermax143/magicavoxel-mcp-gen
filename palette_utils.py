#!/usr/bin/env python3
"""
MagicaVoxel palette utilities - always uses extracted palette
"""

import json
import numpy as np
from pathlib import Path

# Global palette cache
_PALETTE = None

def get_palette():
    """Get the extracted MagicaVoxel palette"""
    global _PALETTE
    if _PALETTE is None:
        palette_path = Path("magica_palette.json")
        if palette_path.exists():
            with open(palette_path, 'r') as f:
                _PALETTE = json.load(f)
        else:
            _PALETTE = get_fallback_palette()
    return _PALETTE

def get_fallback_palette():
    """Fallback standard palette"""
    return [
        [0, 0, 0, 255], [255, 255, 255, 255], [255, 0, 0, 255],
        [0, 255, 0, 255], [0, 0, 255, 255], [255, 255, 0, 255],
        [0, 255, 255, 255], [255, 0, 255, 255]
    ]

def get_color_by_index(index):
    """Get color by palette index"""
    palette = get_palette()
    if 0 <= index < len(palette):
        return palette[index]
    return palette[0]  # Return black if invalid index

def find_closest_color_index(rgb):
    """Find closest color index for RGB values"""
    palette = get_palette()
    min_dist = float('inf')
    best_index = 0
    
    for i, color in enumerate(palette):
        # Ensure color has at least 3 components (RGB)
        color_rgb = color[:3] if len(color) >= 3 else color
        dist = sum((a - b) ** 2 for a, b in zip(rgb, color_rgb))
        if dist < min_dist:
            min_dist = dist
            best_index = i
    
    return best_index
