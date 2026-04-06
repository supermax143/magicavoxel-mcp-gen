#!/usr/bin/env python3
"""
MagicaVoxel MCP Server - Generate voxel models from primitives
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from dataclasses import dataclass
from enum import Enum

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
import pyvox.models
import pyvox.writer
from midvoxio.voxio import viz_vox
import numpy as np

from palette_utils import get_palette, find_closest_color_index

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("magicavoxel-mcp-gen")

# Data structures for scene management
@dataclass
class VoxelObject:
    """Represents a voxel object in the scene"""
    shape_type: str
    dimensions: Tuple[int, int, int]  # (width, height, depth)
    position: Tuple[int, int, int]    # (x, y, z)
    color_hex: str
    color_rgb: Tuple[int, int, int]   # Cached RGB values

class MergeStrategy(Enum):
    SINGLE_OBJECT = "single_object"
    SCENE_GRAPH = "scene_graph"

class MagicaVoxelSession:
    """Manages scene state for complex compositions"""
    
    def __init__(self):
        self.objects: List[VoxelObject] = []
        self.custom_palette: List[Tuple[int, int, int, int]] = []
    
    def add_object(self, obj: VoxelObject):
        """Add object to scene"""
        self.objects.append(obj)
        
        # Add color to custom palette if not present
        if obj.color_rgb not in [c[:3] for c in self.custom_palette]:
            self.custom_palette.append((*obj.color_rgb, 255))
    
    def clear(self):
        """Clear all objects from scene"""
        self.objects = []
        self.custom_palette = []
    
    def get_bounds(self) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """Get scene bounding box (min_pos, max_pos)"""
        if not self.objects:
            return ((0, 0, 0), (0, 0, 0))
        
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        for obj in self.objects:
            x, y, z = obj.position
            w, h, d = obj.dimensions
            
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)
            max_x = max(max_x, x + w)
            max_y = max(max_y, y + h)
            max_z = max(max_z, z + d)
        
        return ((int(min_x), int(min_y), int(min_z)), (int(max_x), int(max_y), int(max_z)))

# Global session instance
session = MagicaVoxelSession()

class VoxelPrimitiveGenerator:
    """Generate voxel primitives using pyvox"""
    
    def __init__(self):
        self.palette = get_palette()
    
    def create_cube(self, size: int, color_rgb: List[int], position: List[int] = [0, 0, 0]) -> pyvox.models.Vox:
        """Create a solid cube"""
        voxels = []
        color_index = find_closest_color_index(color_rgb)
        
        # Avoid index 0 (empty voxels)
        if color_index == 0:
            color_index = 8  # Use dark gray instead
        
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    voxels.append(pyvox.models.Voxel(
                        position[0] + x,
                        position[1] + y, 
                        position[2] + z,
                        color_index
                    ))
        
        model = pyvox.models.Model((size, size, size), voxels)
        return pyvox.models.Vox([model], palette=self.palette)
    
    def create_sphere(self, radius: int, color_rgb: List[int], position: List[int] = [0, 0, 0]) -> pyvox.models.Vox:
        """Create a sphere using midpoint circle algorithm"""
        voxels = []
        color_index = find_closest_color_index(color_rgb)
        
        if color_index == 0:
            color_index = 8
        
        center = radius
        size = radius * 2 + 1
        
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    # Calculate distance from center
                    dx = x - center
                    dy = y - center  
                    dz = z - center
                    distance = (dx*dx + dy*dy + dz*dz) ** 0.5
                    
                    if distance <= radius:
                        voxels.append(pyvox.models.Voxel(
                            position[0] + x,
                            position[1] + y,
                            position[2] + z,
                            color_index
                        ))
        
        model = pyvox.models.Model((size, size, size), voxels)
        return pyvox.models.Vox([model], palette=self.palette)
    
    def create_cylinder(self, radius: int, height: int, color_rgb: List[int], position: List[int] = [0, 0, 0]) -> pyvox.models.Vox:
        """Create a cylinder"""
        voxels = []
        color_index = find_closest_color_index(color_rgb)
        
        if color_index == 0:
            color_index = 8
        
        size_x = radius * 2 + 1
        size_z = radius * 2 + 1
        center_x = radius
        center_z = radius
        
        for x in range(size_x):
            for y in range(height):
                for z in range(size_z):
                    # Calculate distance from center in XZ plane
                    dx = x - center_x
                    dz = z - center_z
                    distance = (dx*dx + dz*dz) ** 0.5
                    
                    if distance <= radius:
                        voxels.append(pyvox.models.Voxel(
                            position[0] + x,
                            position[1] + y,
                            position[2] + z,
                            color_index
                        ))
        
        model = pyvox.models.Model((size_x, height, size_z), voxels)
        return pyvox.models.Vox([model], palette=self.palette)
    
    def create_pyramid(self, base_size: int, height: int, color_rgb: List[int], position: List[int] = [0, 0, 0]) -> pyvox.models.Vox:
        """Create a pyramid"""
        voxels = []
        color_index = find_closest_color_index(color_rgb)
        
        if color_index == 0:
            color_index = 8
        
        for y in range(height):
            # Calculate layer size (pyramid gets smaller as it goes up)
            layer_size = base_size - int((base_size * y) / height)
            if layer_size <= 0:
                continue
                
            offset = (base_size - layer_size) // 2
            
            for x in range(layer_size):
                for z in range(layer_size):
                    voxels.append(pyvox.models.Voxel(
                        position[0] + offset + x,
                        position[1] + y,
                        position[2] + offset + z,
                        color_index
                    ))
        
        model = pyvox.models.Model((base_size, height, base_size), voxels)
        return pyvox.models.Vox([model], palette=self.palette)
    
    def generate_object_voxels(self, obj: VoxelObject) -> List[pyvox.models.Voxel]:
        """Generate voxels for a VoxelObject based on its shape type"""
        voxels = []
        color_index = find_closest_color_index(list(obj.color_rgb))
        
        if color_index == 0:
            color_index = 8
        
        x_offset, y_offset, z_offset = obj.position
        w, h, d = obj.dimensions
        
        if obj.shape_type == "cube":
            for x in range(w):
                for y in range(h):
                    for z in range(d):
                        voxels.append(pyvox.models.Voxel(
                            x_offset + x,
                            y_offset + y,
                            z_offset + z,
                            color_index
                        ))
        
        elif obj.shape_type == "sphere":
            center_x = w // 2
            center_y = h // 2
            center_z = d // 2
            max_radius = min(w, h, d) // 2
            
            for x in range(w):
                for y in range(h):
                    for z in range(d):
                        dx = x - center_x
                        dy = y - center_y
                        dz = z - center_z
                        distance = (dx*dx + dy*dy + dz*dz) ** 0.5
                        
                        if distance <= max_radius:
                            voxels.append(pyvox.models.Voxel(
                                x_offset + x,
                                y_offset + y,
                                z_offset + z,
                                color_index
                            ))
        
        elif obj.shape_type == "cylinder":
            radius = min(w, d) // 2
            center_x = w // 2
            center_z = d // 2
            
            for x in range(w):
                for y in range(h):
                    for z in range(d):
                        dx = x - center_x
                        dz = z - center_z
                        distance = (dx*dx + dz*dz) ** 0.5
                        
                        if distance <= radius:
                            voxels.append(pyvox.models.Voxel(
                                x_offset + x,
                                y_offset + y,
                                z_offset + z,
                                color_index
                            ))
        
        elif obj.shape_type == "pyramid":
            for y in range(h):
                layer_size = w - int((w * y) / h)
                if layer_size <= 0:
                    continue
                    
                offset = (w - layer_size) // 2
                
                for x in range(layer_size):
                    for z in range(layer_size):
                        voxels.append(pyvox.models.Voxel(
                            x_offset + offset + x,
                            y_offset + y,
                            z_offset + offset + z,
                            color_index
                        ))
        
        return voxels
    
    def combine_objects(self, objects: List[VoxelObject], merge_strategy: MergeStrategy) -> pyvox.models.Vox:
        """Combine multiple objects into a single VOX model"""
        if not objects:
            raise ValueError("No objects to combine")
        
        if merge_strategy == MergeStrategy.SINGLE_OBJECT:
            return self._combine_single_object(objects)
        elif merge_strategy == MergeStrategy.SCENE_GRAPH:
            return self._combine_scene_graph(objects)
        else:
            raise ValueError(f"Unknown merge strategy: {merge_strategy}")
    
    def _combine_single_object(self, objects: List[VoxelObject]) -> pyvox.models.Vox:
        """Combine all objects into a single model"""
        all_voxels = []
        
        for obj in objects:
            voxels = self.generate_object_voxels(obj)
            all_voxels.extend(voxels)
        
        # Calculate bounding box
        min_pos, max_pos = session.get_bounds()
        size = (
            max_pos[0] - min_pos[0],
            max_pos[1] - min_pos[1],
            max_pos[2] - min_pos[2]
        )
        
        # Adjust voxel positions to be relative to min_pos
        adjusted_voxels = []
        for voxel in all_voxels:
            adjusted_voxels.append(pyvox.models.Voxel(
                voxel.x - min_pos[0],
                voxel.y - min_pos[1],
                voxel.z - min_pos[2],
                voxel.c
            ))
        
        model = pyvox.models.Model(size, adjusted_voxels)
        return pyvox.models.Vox([model], palette=self.palette)
    
    def _combine_scene_graph(self, objects: List[VoxelObject]) -> pyvox.models.Vox:
        """Create scene graph with separate models for each object"""
        models = []
        
        for obj in objects:
            voxels = self.generate_object_voxels(obj)
            model = pyvox.models.Model(obj.dimensions, voxels)
            models.append(model)
        
        return pyvox.models.Vox(models, palette=self.palette)
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")
        
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError as e:
            raise ValueError(f"Invalid hex color: {hex_color}") from e

# Initialize generator
generator = VoxelPrimitiveGenerator()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="add_primitive_to_scene",
            description="Add a primitive to the current scene composition",
            inputSchema={
                "type": "object",
                "properties": {
                    "shape_type": {
                        "type": "string",
                        "enum": ["cube", "sphere", "cylinder", "pyramid"],
                        "description": "Type of primitive shape"
                    },
                    "dimensions": {
                        "type": "object",
                        "properties": {
                            "width": {"type": "integer", "minimum": 1, "maximum": 64},
                            "height": {"type": "integer", "minimum": 1, "maximum": 64},
                            "depth": {"type": "integer", "minimum": 1, "maximum": 64}
                        },
                        "required": ["width", "height", "depth"],
                        "description": "Object dimensions (width, height, depth)"
                    },
                    "position": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"},
                            "z": {"type": "integer"}
                        },
                        "required": ["x", "y", "z"],
                        "description": "Position relative to scene center (x, y, z)"
                    },
                    "color_hex": {
                        "type": "string",
                        "pattern": "^#[0-9A-Fa-f]{6}$",
                        "description": "Color in hex format #RRGGBB"
                    }
                },
                "required": ["shape_type", "dimensions", "position", "color_hex"]
            }
        ),
        types.Tool(
            name="combine_and_export",
            description="Combine all scene objects and export to VOX file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Output filename for the combined model"
                    },
                    "output_directory": {
                        "type": "string",
                        "description": "Directory path where to save the file (default: current directory)"
                    },
                    "merge_strategy": {
                        "type": "string",
                        "enum": ["single_object", "scene_graph"],
                        "default": "single_object",
                        "description": "How to combine objects: single_object (one model) or scene_graph (separate models)"
                    }
                },
                "required": ["filename"]
            }
        ),
        types.Tool(
            name="clear_scene",
            description="Clear all objects from the current scene",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="list_scene_objects",
            description="List all objects currently in the scene",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_scene_bounds",
            description="Get the bounding box of the current scene",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="create_cube",
            description="Create a voxel cube",
            inputSchema={
                "type": "object",
                "properties": {
                    "size": {
                        "type": "integer",
                        "description": "Size of the cube (width=height=depth)",
                        "minimum": 1,
                        "maximum": 64
                    },
                    "color": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "RGB color values [r, g, b] (0-255)"
                    },
                    "position": {
                        "type": "array", 
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "Position [x, y, z] (default: [0, 0, 0])"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (default: cube.vox)"
                    },
                    "output_directory": {
                        "type": "string",
                        "description": "Directory path where to save the file (default: current directory)"
                    }
                },
                "required": ["size", "color"]
            }
        ),
        types.Tool(
            name="create_sphere",
            description="Create a voxel sphere",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "integer",
                        "description": "Radius of the sphere",
                        "minimum": 1,
                        "maximum": 32
                    },
                    "color": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "RGB color values [r, g, b] (0-255)"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "Position [x, y, z] (default: [0, 0, 0])"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (default: sphere.vox)"
                    }
                },
                "required": ["radius", "color"]
            }
        ),
        types.Tool(
            name="create_cylinder",
            description="Create a voxel cylinder",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "integer",
                        "description": "Radius of the cylinder",
                        "minimum": 1,
                        "maximum": 32
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height of the cylinder",
                        "minimum": 1,
                        "maximum": 64
                    },
                    "color": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "RGB color values [r, g, b] (0-255)"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "Position [x, y, z] (default: [0, 0, 0])"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (default: cylinder.vox)"
                    }
                },
                "required": ["radius", "height", "color"]
            }
        ),
        types.Tool(
            name="create_pyramid",
            description="Create a voxel pyramid",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_size": {
                        "type": "integer",
                        "description": "Size of the pyramid base",
                        "minimum": 1,
                        "maximum": 64
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height of the pyramid",
                        "minimum": 1,
                        "maximum": 64
                    },
                    "color": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "RGB color values [r, g, b] (0-255)"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "Position [x, y, z] (default: [0, 0, 0])"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (default: pyramid.vox)"
                    }
                },
                "required": ["base_size", "height", "color"]
            }
        ),
        types.Tool(
            name="visualize_vox",
            description="Visualize a VOX file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to VOX file to visualize"
                    }
                },
                "required": ["filename"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls"""
    try:
        # New scene composition tools
        if name == "add_primitive_to_scene":
            shape_type = arguments["shape_type"]
            dimensions = arguments["dimensions"]
            position = arguments["position"]
            color_hex = arguments["color_hex"]
            
            # Convert to proper format
            dims = (dimensions["width"], dimensions["height"], dimensions["depth"])
            pos = (position["x"], position["y"], position["z"])
            color_rgb = generator.hex_to_rgb(color_hex)
            
            # Create and add object
            obj = VoxelObject(
                shape_type=shape_type,
                dimensions=dims,
                position=pos,
                color_hex=color_hex,
                color_rgb=color_rgb
            )
            
            session.add_object(obj)
            
            return [types.TextContent(
                type="text",
                text=f"Added {shape_type} to scene at position {pos} with color {color_hex}"
            )]
        
        elif name == "combine_and_export":
            filename = arguments["filename"]
            output_directory = arguments.get("output_directory", ".")
            merge_strategy_str = arguments.get("merge_strategy", "single_object")
            
            if not session.objects:
                return [types.TextContent(
                    type="text",
                    text="Error: No objects in scene to export"
                )]
            
            # Create output directory if it doesn't exist
            import os
            try:
                os.makedirs(output_directory, exist_ok=True)
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error creating directory {output_directory}: {str(e)}"
                )]
            
            # Construct full file path
            full_path = os.path.join(output_directory, filename)
            
            # Convert merge strategy
            merge_strategy = MergeStrategy.SINGLE_OBJECT if merge_strategy_str == "single_object" else MergeStrategy.SCENE_GRAPH
            
            # Combine and export
            vox = generator.combine_objects(session.objects, merge_strategy)
            writer = pyvox.writer.VoxWriter(full_path, vox)
            writer.write()
            
            return [types.TextContent(
                type="text",
                text=f"Exported {len(session.objects)} objects to {full_path} using {merge_strategy_str} strategy"
            )]
        
        elif name == "clear_scene":
            session.clear()
            return [types.TextContent(
                type="text",
                text="Scene cleared"
            )]
        
        elif name == "list_scene_objects":
            if not session.objects:
                return [types.TextContent(
                    type="text",
                    text="No objects in scene"
                )]
            
            obj_list = []
            for i, obj in enumerate(session.objects):
                obj_list.append(f"{i+1}. {obj.shape_type} at {obj.position} ({obj.color_hex})")
            
            return [types.TextContent(
                type="text",
                text=f"Scene objects ({len(session.objects)}):\n" + "\n".join(obj_list)
            )]
        
        elif name == "get_scene_bounds":
            if not session.objects:
                return [types.TextContent(
                    type="text",
                    text="No objects in scene"
                )]
            
            min_pos, max_pos = session.get_bounds()
            size = (
                max_pos[0] - min_pos[0],
                max_pos[1] - min_pos[1],
                max_pos[2] - min_pos[2]
            )
            
            return [types.TextContent(
                type="text",
                text=f"Scene bounds:\nMin: {min_pos}\nMax: {max_pos}\nSize: {size}"
            )]
        
        elif name == "create_cube":
            size = arguments["size"]
            color = arguments["color"]
            position = arguments.get("position", [0, 0, 0])
            filename = arguments.get("filename", "cube.vox")
            output_directory = arguments.get("output_directory", ".")
            
            # Create output directory if it doesn't exist
            import os
            try:
                os.makedirs(output_directory, exist_ok=True)
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error creating directory {output_directory}: {str(e)}"
                )]
            
            # Construct full file path
            full_path = os.path.join(output_directory, filename)
            
            vox = generator.create_cube(size, color, position)
            writer = pyvox.writer.VoxWriter(full_path, vox)
            writer.write()
            
            return [types.TextContent(
                type="text",
                text=f"Created cube: {full_path} (size: {size}, color: {color}, position: {position})"
            )]
        
        elif name == "create_sphere":
            radius = arguments["radius"]
            color = arguments["color"]
            position = arguments.get("position", [0, 0, 0])
            filename = arguments.get("filename", "sphere.vox")
            
            vox = generator.create_sphere(radius, color, position)
            writer = pyvox.writer.VoxWriter(filename, vox)
            writer.write()
            
            return [types.TextContent(
                type="text",
                text=f"Created sphere: {filename} (radius: {radius}, color: {color}, position: {position})"
            )]
        
        elif name == "create_cylinder":
            radius = arguments["radius"]
            height = arguments["height"]
            color = arguments["color"]
            position = arguments.get("position", [0, 0, 0])
            filename = arguments.get("filename", "cylinder.vox")
            
            vox = generator.create_cylinder(radius, height, color, position)
            writer = pyvox.writer.VoxWriter(filename, vox)
            writer.write()
            
            return [types.TextContent(
                type="text",
                text=f"Created cylinder: {filename} (radius: {radius}, height: {height}, color: {color}, position: {position})"
            )]
        
        elif name == "create_pyramid":
            base_size = arguments["base_size"]
            height = arguments["height"]
            color = arguments["color"]
            position = arguments.get("position", [0, 0, 0])
            filename = arguments.get("filename", "pyramid.vox")
            
            vox = generator.create_pyramid(base_size, height, color, position)
            writer = pyvox.writer.VoxWriter(filename, vox)
            writer.write()
            
            return [types.TextContent(
                type="text",
                text=f"Created pyramid: {filename} (base_size: {base_size}, height: {height}, color: {color}, position: {position})"
            )]
        
        elif name == "visualize_vox":
            filename = arguments["filename"]
            if not Path(filename).exists():
                return [types.TextContent(
                    type="text",
                    text=f"Error: File {filename} not found"
                )]
            
            viz_vox(filename)
            return [types.TextContent(
                type="text",
                text=f"Visualized: {filename}"
            )]
        
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error in {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Main server loop"""
    # Use stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
