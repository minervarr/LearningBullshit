#!/usr/bin/env python3
"""
SVG Grid Organizer
Arranges 8 SVG files into a grid layout and creates a combined SVG output.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def get_svg_dimensions(svg_path):
    """Extract width and height from an SVG file."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Remove namespace if present
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'
        else:
            namespace = ''

        width = root.get('width', '100')
        height = root.get('height', '100')

        # Remove units if present (px, pt, etc.)
        width = ''.join(filter(lambda x: x.isdigit() or x == '.', width))
        height = ''.join(filter(lambda x: x.isdigit() or x == '.', height))

        return float(width) if width else 100.0, float(height) if height else 100.0
    except Exception as e:
        print(f"Warning: Could not parse {svg_path}: {e}")
        return 100.0, 100.0


def create_svg_grid(svg_files, output_file, rows=2, cols=4, cell_width=200, cell_height=200, padding=10):
    """
    Create a grid layout of SVG files.

    Args:
        svg_files: List of paths to SVG files (should be 8 files)
        output_file: Output path for the combined SVG
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        cell_width: Width of each cell in pixels
        cell_height: Height of each cell in pixels
        padding: Padding between cells in pixels
    """
    if len(svg_files) != rows * cols:
        print(f"Warning: Expected {rows * cols} files for a {rows}x{cols} grid, got {len(svg_files)}")

    # Calculate total dimensions
    total_width = cols * cell_width + (cols - 1) * padding
    total_height = rows * cell_height + (rows - 1) * padding

    # Start building the SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}">
'''

    # Add a background
    svg_content += f'  <rect width="{total_width}" height="{total_height}" fill="#f0f0f0"/>\n\n'

    # Place each SVG in the grid
    for idx, svg_file in enumerate(svg_files):
        if idx >= rows * cols:
            break

        row = idx // cols
        col = idx % cols

        x = col * (cell_width + padding)
        y = row * (cell_height + padding)

        # Read the SVG content
        try:
            with open(svg_file, 'r', encoding='utf-8') as f:
                svg_data = f.read()

            # Extract just the inner content (remove svg tags)
            tree = ET.fromstring(svg_data)

            # Get original dimensions for scaling
            orig_width, orig_height = get_svg_dimensions(svg_file)

            # Calculate scale to fit in cell (with some margin)
            margin = 10
            scale_x = (cell_width - 2 * margin) / orig_width if orig_width > 0 else 1
            scale_y = (cell_height - 2 * margin) / orig_height if orig_height > 0 else 1
            scale = min(scale_x, scale_y)

            # Center the SVG in the cell
            scaled_width = orig_width * scale
            scaled_height = orig_height * scale
            offset_x = x + (cell_width - scaled_width) / 2
            offset_y = y + (cell_height - scaled_height) / 2

            # Add a cell background
            svg_content += f'  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="white" stroke="#ccc" stroke-width="1"/>\n'

            # Add the SVG as a group with transform
            svg_content += f'  <g transform="translate({offset_x}, {offset_y}) scale({scale})">\n'

            # Add inner SVG elements
            for child in tree:
                svg_content += '    ' + ET.tostring(child, encoding='unicode') + '\n'

            svg_content += '  </g>\n\n'

            # Add filename label
            filename = os.path.basename(svg_file)
            text_y = y + cell_height - 5
            svg_content += f'  <text x="{x + cell_width/2}" y="{text_y}" text-anchor="middle" font-size="10" fill="#666">{filename}</text>\n\n'

        except Exception as e:
            print(f"Error processing {svg_file}: {e}")
            # Add error placeholder
            svg_content += f'  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="#ffcccc" stroke="red"/>\n'
            svg_content += f'  <text x="{x + cell_width/2}" y="{y + cell_height/2}" text-anchor="middle" fill="red">Error loading file</text>\n\n'

    svg_content += '</svg>'

    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✓ Created grid SVG: {output_file}")
    print(f"  Dimensions: {total_width}x{total_height}px")
    print(f"  Grid: {rows}x{cols}")
    print(f"  Files processed: {len(svg_files)}")


def main():
    """Main function to run the SVG grid organizer."""
    if len(sys.argv) < 2:
        print("Usage: python svg_grid_organizer.py <svg_file1> <svg_file2> ... <svg_file8> [output.svg]")
        print("\nOptions:")
        print("  You can also use: python svg_grid_organizer.py *.svg")
        print("\nExample:")
        print("  python svg_grid_organizer.py file1.svg file2.svg file3.svg file4.svg file5.svg file6.svg file7.svg file8.svg output.svg")
        print("  python svg_grid_organizer.py *.svg")
        sys.exit(1)

    # Get SVG files from arguments
    svg_files = []
    output_file = "grid_output.svg"

    for arg in sys.argv[1:]:
        if arg.endswith('.svg'):
            if os.path.exists(arg):
                svg_files.append(arg)
            else:
                # This might be the output file
                if len(svg_files) >= 8:
                    output_file = arg
        else:
            print(f"Warning: Skipping non-SVG file: {arg}")

    # If we have more than 8 files, the last one might be the output
    if len(svg_files) > 8:
        output_file = svg_files[-1]
        svg_files = svg_files[:8]

    if len(svg_files) < 8:
        print(f"Warning: Found only {len(svg_files)} SVG files. Grid may have empty spaces.")
        # Fill with empty placeholders if needed
        while len(svg_files) < 8:
            svg_files.append(None)
    elif len(svg_files) > 8:
        print(f"Warning: Found {len(svg_files)} SVG files. Using only the first 8.")
        svg_files = svg_files[:8]

    # Filter out None values
    svg_files = [f for f in svg_files if f is not None]

    if not svg_files:
        print("Error: No valid SVG files found!")
        sys.exit(1)

    print(f"Processing {len(svg_files)} SVG files...")
    for i, f in enumerate(svg_files, 1):
        print(f"  {i}. {f}")

    # Create the grid (2 rows x 4 columns)
    create_svg_grid(svg_files, output_file, rows=2, cols=4)

    print(f"\n✓ Done! Open {output_file} to view the result.")


if __name__ == "__main__":
    main()
