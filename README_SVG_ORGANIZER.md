# SVG Grid Organizer

A Python script to organize 8 SVG files into a grid layout (2 rows × 4 columns).

## Features

- Arranges 8 SVG files into a 2x4 grid
- Automatically scales SVG files to fit each cell
- Adds labels with filenames
- Creates a single combined SVG output file

## Requirements

- Python 3.x (no external dependencies needed)

## Usage

### Basic Usage

```bash
python svg_grid_organizer.py file1.svg file2.svg file3.svg file4.svg file5.svg file6.svg file7.svg file8.svg
```

This creates `grid_output.svg` with all 8 files arranged in a grid.

### Specify Output File

```bash
python svg_grid_organizer.py file1.svg file2.svg file3.svg file4.svg file5.svg file6.svg file7.svg file8.svg my_grid.svg
```

### Using Wildcards

```bash
python svg_grid_organizer.py *.svg
```

This will use the first 8 SVG files found in the current directory.

## Example

```bash
# Create sample SVG files (for testing)
./svg_grid_organizer.py icon1.svg icon2.svg icon3.svg icon4.svg icon5.svg icon6.svg icon7.svg icon8.svg output.svg
```

## Output

The script creates a single SVG file containing:
- A 2×4 grid layout (8 cells)
- Each SVG file scaled to fit within its cell
- Filename labels below each cell
- White cell backgrounds with gray borders

## Customization

To change the grid layout, cell size, or padding, edit the parameters in the `create_svg_grid()` function call in `main()`:

```python
create_svg_grid(svg_files, output_file,
                rows=2,           # Number of rows
                cols=4,           # Number of columns
                cell_width=200,   # Cell width in pixels
                cell_height=200,  # Cell height in pixels
                padding=10)       # Padding between cells
```

## Notes

- The script expects exactly 8 SVG files
- If fewer files are provided, empty spaces will appear in the grid
- If more than 8 files are provided, only the first 8 will be used
- SVG files are automatically centered and scaled to fit within each cell
