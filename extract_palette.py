#!/usr/bin/env python3
"""
Extract colors from MagicaVoxel palette PNG file and save as reusable palette
"""

import numpy as np
from PIL import Image
import json

def extract_palette_from_png(palette_path, output_path=None):
    """
    Extract colors from palette PNG file and save as JSON palette
    
    Args:
        palette_path: Path to PNG palette file
        output_path: Path to save JSON palette (optional)
    
    Returns:
        List of colors in [[r, g, b, a], ...] format
    """
    try:
        # Open palette image
        img = Image.open(palette_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image data as numpy array
        img_array = np.array(img)
        
        # Extract unique colors
        # Flatten the array and get unique rows
        pixels = img_array.reshape(-1, 4)
        unique_colors = np.unique(pixels, axis=0)
        
        # Filter out transparent/empty pixels (alpha = 0)
        valid_colors = [color.tolist() for color in unique_colors if color[3] > 0]
        
        # Sort by brightness for better organization
        valid_colors.sort(key=lambda x: sum(x[:3]))
        
        # Ensure we have at least basic colors
        if len(valid_colors) < 8:
            # Add standard MagicaVoxel colors if missing
            standard_colors = [
                [0, 0, 0, 255],      # Black
                [255, 255, 255, 255], # White  
                [255, 0, 0, 255],     # Red
                [0, 255, 0, 255],     # Green
                [0, 0, 255, 255],     # Blue
                [255, 255, 0, 255],   # Yellow
                [0, 255, 255, 255],   # Cyan
                [255, 0, 255, 255],   # Magenta
            ]
            
            existing_rgb = set(tuple(color[:3]) for color in valid_colors)
            for std_color in standard_colors:
                if tuple(std_color[:3]) not in existing_rgb:
                    valid_colors.append(std_color)
        
        # Save to JSON if output path provided
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(valid_colors, f, indent=2)
            print(f"Palette saved to {output_path}")
        
        print(f"Extracted {len(valid_colors)} colors from palette")
        return valid_colors
        
    except Exception as e:
        print(f"Error extracting palette: {e}")
        # Return standard palette as fallback
        return [
            [0, 0, 0, 255],      # Black
            [255, 255, 255, 255], # White  
            [255, 0, 0, 255],     # Red
            [0, 255, 0, 255],     # Green
            [0, 0, 255, 255],     # Blue
            [255, 255, 0, 255],   # Yellow
            [0, 255, 255, 255],   # Cyan
            [255, 0, 255, 255],   # Magenta
        ]

def load_palette(palette_path):
    """Load palette from JSON file"""
    try:
        with open(palette_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading palette: {e}")
        return None

def get_standard_palette():
    """Get standard MagicaVoxel palette"""
    return [
        [0, 0, 0, 255],        # Index 0: Black
        [255, 255, 255, 255],  # Index 1: White
        [255, 0, 0, 255],      # Index 2: Red
        [0, 255, 0, 255],      # Index 3: Green
        [0, 0, 255, 255],      # Index 4: Blue
        [255, 255, 0, 255],    # Index 5: Yellow
        [0, 255, 255, 255],    # Index 6: Cyan
        [255, 0, 255, 255],    # Index 7: Magenta
        [128, 128, 128, 255],  # Index 8: Gray
        [64, 64, 64, 255],     # Index 9: Dark Gray
        [192, 192, 192, 255],  # Index 10: Light Gray
        [255, 128, 0, 255],    # Index 11: Orange
        [128, 255, 0, 255],    # Index 12: Lime
        [0, 128, 255, 255],    # Index 13: Sky Blue
        [128, 0, 255, 255],    # Index 14: Purple
        [255, 0, 128, 255],    # Index 15: Pink
    ]

if __name__ == "__main__":
    # Extract palette from PNG
    palette_path = "Pallet/pallet.png"
    output_path = "magica_palette.json"
    
    palette = extract_palette_from_png(palette_path, output_path)
    
    print("\nExtracted palette:")
    for i, color in enumerate(palette):
        print(f"Index {i}: RGBA{tuple(color)}")
