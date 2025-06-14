#!/usr/bin/env python3
"""
3D Auxetic Capacitive Sensor - CadQuery Model

This script generates a complete 3D model of a capacitive pressure sensor
based on re-entrant auxetic lattice structures, ready for 3D printing.

Requirements:
    pip install cadquery-ocp
    
Usage:
    python auxetic_cell_3d.py
    
Output:
    - auxetic_sensor.step (CAD file)
    - auxetic_sensor.stl (3D printing file)
    - auxetic_unit_cell.stl (single cell for testing)
"""

import cadquery as cq
import math
import sys
import os

# Add src directory for our design functions
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from design import generate_reentrant_cell, calculate_poisson_ratio

class AuxeticSensor3D:
    """3D model generator for auxetic capacitive sensor."""
    
    def __init__(self, 
                 cell_size: float = 10.0,      # mm - unit cell size
                 wall_thickness: float = 1.0,   # mm - strut thickness  
                 alpha: float = 45.0,           # degrees - re-entrance angle
                 height: float = 3.0,           # mm - sensor thickness
                 nx: int = 3,                   # number of cells in x
                 ny: int = 3,                   # number of cells in y
                 electrode_thickness: float = 0.2,  # mm - capacitor plates
                 gap: float = 1.0):             # mm - capacitor gap
        """
        Initialize 3D auxetic sensor parameters.
        
        Parameters
        ----------
        cell_size : float
            Size of individual auxetic unit cell (mm).
        wall_thickness : float  
            Thickness of auxetic struts (mm).
        alpha : float
            Re-entrance angle in degrees.
        height : float
            Total sensor thickness (mm).
        nx, ny : int
            Number of unit cells in x and y directions.
        electrode_thickness : float
            Thickness of capacitor electrode plates (mm).
        gap : float
            Gap between capacitor plates (mm).
        """
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.alpha = alpha
        self.height = height
        self.nx = nx
        self.ny = ny
        self.electrode_thickness = electrode_thickness
        self.gap = gap
        
        # Calculate derived parameters
        self.poisson_ratio = calculate_poisson_ratio(1.0, alpha)
        self.total_width = nx * cell_size
        self.total_length = ny * cell_size
        
        print(f"🔧 Auxetic Sensor Parameters:")
        print(f"   Cell size: {cell_size} mm")
        print(f"   Re-entrance angle: {alpha}°")
        print(f"   Poisson's ratio: {self.poisson_ratio:.3f}")
        print(f"   Array: {nx}×{ny} cells")
        print(f"   Total dimensions: {self.total_width}×{self.total_length}×{height} mm")
    
    def create_unit_cell_2d(self) -> cq.Workplane:
        """Create a 2D profile of a single auxetic unit cell."""
        
        # Get 2D cell geometry from our design function
        cell_data = generate_reentrant_cell(
            a=self.cell_size/10,  # Convert to design units (cm)
            b=self.wall_thickness/10, 
            alpha=self.alpha
        )
        
        nodes = [(x*10, y*10) for x, y in cell_data["nodes"]]  # Convert to mm
        edges = cell_data["edges"]
        
        # Create the cell profile using CadQuery
        # Start with the first edge
        start_edge = edges[0]
        start_node = nodes[start_edge[0]]
        
        # Create a wire from the edges
        points = []
        for edge in edges:
            start_idx, end_idx = edge
            if not points:  # First edge
                points.append(nodes[start_idx])
            points.append(nodes[end_idx])
        
        # Close the loop
        if points[-1] != points[0]:
            points.append(points[0])
        
        # Create the 2D profile
        profile = cq.Workplane("XY").polyline(points).close()
        
        return profile
    
    def create_unit_cell_3d(self) -> cq.Workplane:
        """Create a 3D auxetic unit cell."""
        
        # Create 2D profile and extrude
        profile = self.create_unit_cell_2d()
        cell_3d = profile.extrude(self.height)
        
        return cell_3d
    
    def create_auxetic_array(self) -> cq.Workplane:
        """Create an array of auxetic unit cells."""
        
        # Create single unit cell
        unit_cell = self.create_unit_cell_3d()
        
        # Create array by copying and translating
        array = cq.Workplane("XY")
        
        for i in range(self.nx):
            for j in range(self.ny):
                # Calculate position
                x_pos = i * self.cell_size
                y_pos = j * self.cell_size
                
                # Add translated cell to array
                translated_cell = unit_cell.translate((x_pos, y_pos, 0))
                array = array.union(translated_cell)
        
        return array
    
    def create_capacitor_plates(self) -> tuple[cq.Workplane, cq.Workplane]:
        """Create top and bottom capacitor electrode plates."""
        
        plate_width = self.total_width + 5  # mm - extend beyond auxetic structure
        plate_length = self.total_length + 5
        
        # Bottom plate
        bottom_plate = (cq.Workplane("XY")
                       .box(plate_width, plate_length, self.electrode_thickness)
                       .translate((self.total_width/2, self.total_length/2, 
                                 -self.electrode_thickness/2)))
        
        # Top plate  
        top_plate = (cq.Workplane("XY")
                    .box(plate_width, plate_length, self.electrode_thickness)
                    .translate((self.total_width/2, self.total_length/2, 
                              self.height + self.gap + self.electrode_thickness/2)))
        
        return bottom_plate, top_plate
    
    def create_support_posts(self) -> cq.Workplane:
        """Create support posts to maintain capacitor gap."""
        
        post_diameter = 1.0  # mm
        post_height = self.height + self.gap
        
        # Place posts at corners and center
        post_positions = [
            (2, 2),  # Corner posts
            (self.total_width-2, 2),
            (2, self.total_length-2), 
            (self.total_width-2, self.total_length-2),
            (self.total_width/2, self.total_length/2)  # Center post
        ]
        
        posts = cq.Workplane("XY")
        
        for x, y in post_positions:
            post = (cq.Workplane("XY")
                   .circle(post_diameter/2)
                   .extrude(post_height)
                   .translate((x, y, 0)))
            posts = posts.union(post)
        
        return posts
    
    def create_wire_channels(self) -> cq.Workplane:
        """Create channels for electrical connections."""
        
        channel_width = 2.0  # mm
        channel_depth = 0.5  # mm
        
        # Bottom plate wire channel
        bottom_channel = (cq.Workplane("XY")
                         .rect(channel_width, self.total_length + 10)
                         .extrude(channel_depth)
                         .translate((-2.5, self.total_length/2, 
                                   -self.electrode_thickness)))
        
        # Top plate wire channel  
        top_channel = (cq.Workplane("XY")
                      .rect(channel_width, self.total_length + 10)
                      .extrude(channel_depth)
                      .translate((self.total_width + 2.5, self.total_length/2,
                                self.height + self.gap + self.electrode_thickness)))
        
        return bottom_channel.union(top_channel)
    
    def create_complete_sensor(self) -> cq.Workplane:
        """Create the complete auxetic capacitive sensor assembly."""
        
        print("🏗️  Building auxetic structure...")
        auxetic_structure = self.create_auxetic_array()
        
        print("🔌 Adding capacitor plates...")
        bottom_plate, top_plate = self.create_capacitor_plates()
        
        print("🏛️  Adding support posts...")
        support_posts = self.create_support_posts()
        
        print("⚡ Creating wire channels...")
        wire_channels = self.create_wire_channels()
        
        # Combine all components
        complete_sensor = (auxetic_structure
                          .union(bottom_plate)
                          .union(top_plate)
                          .union(support_posts)
                          .cut(wire_channels))  # Cut channels for wires
        
        return complete_sensor
    
    def export_models(self, output_dir: str = "cad"):
        """Export 3D models in various formats."""
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("🚀 Generating complete sensor model...")
        complete_sensor = self.create_complete_sensor()
        
        print("💾 Exporting files...")
        
        # Export complete sensor
        step_file = os.path.join(output_dir, "auxetic_sensor.step")
        stl_file = os.path.join(output_dir, "auxetic_sensor.stl")
        
        cq.exporters.export(complete_sensor, step_file)
        cq.exporters.export(complete_sensor, stl_file)
        
        print(f"✅ Exported: {step_file}")
        print(f"✅ Exported: {stl_file}")
        
        # Export single unit cell for testing
        print("🔬 Generating unit cell...")
        unit_cell = self.create_unit_cell_3d()
        unit_cell_file = os.path.join(output_dir, "auxetic_unit_cell.stl")
        cq.exporters.export(unit_cell, unit_cell_file)
        print(f"✅ Exported: {unit_cell_file}")
        
        # Generate manufacturing info
        self.generate_manufacturing_info(output_dir)
        
        return step_file, stl_file, unit_cell_file
    
    def generate_manufacturing_info(self, output_dir: str):
        """Generate manufacturing and assembly instructions."""
        
        info_file = os.path.join(output_dir, "manufacturing_info.txt")
        
        with open(info_file, 'w') as f:
            f.write("AUXETIC CAPACITIVE SENSOR - Manufacturing Information\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("DESIGN PARAMETERS:\n")
            f.write(f"  • Cell size: {self.cell_size} mm\n")
            f.write(f"  • Wall thickness: {self.wall_thickness} mm\n") 
            f.write(f"  • Re-entrance angle: {self.alpha}°\n")
            f.write(f"  • Poisson's ratio: {self.poisson_ratio:.3f}\n")
            f.write(f"  • Array size: {self.nx}×{self.ny} cells\n")
            f.write(f"  • Total dimensions: {self.total_width}×{self.total_length}×{self.height} mm\n")
            f.write(f"  • Capacitor gap: {self.gap} mm\n\n")
            
            f.write("3D PRINTING SETTINGS:\n")
            f.write("  • Layer height: 0.2 mm (recommended)\n")
            f.write("  • Infill: 100% (solid for mechanical properties)\n")
            f.write("  • Support: Yes (for overhangs in auxetic structure)\n")
            f.write("  • Material: PLA or PETG (conductive filament for electrodes)\n")
            f.write("  • Nozzle: 0.4 mm\n")
            f.write("  • Print speed: 50 mm/s (for precision)\n\n")
            
            f.write("ASSEMBLY INSTRUCTIONS:\n")
            f.write("  1. Print the complete sensor model\n")
            f.write("  2. Remove support material carefully\n")
            f.write("  3. Test auxetic deformation by gentle compression\n")
            f.write("  4. Connect wires to electrode plates via channels\n")
            f.write("  5. Seal wire channels with flexible adhesive\n")
            f.write("  6. Calibrate using known loads (see test_setup.py)\n\n")
            
            f.write("TESTING:\n")
            f.write("  • Use multimeter to verify capacitance (~pF range)\n")
            f.write("  • Apply gentle pressure and observe capacitance change\n")
            f.write("  • Expected behavior: capacitance increases under compression\n")
            f.write("  • Use Python scripts in ../src/ for data analysis\n\n")
            
            f.write("TROUBLESHOOTING:\n")
            f.write("  • If struts break: increase wall_thickness parameter\n")
            f.write("  • If no capacitance change: check electrical connections\n")
            f.write("  • If too stiff: decrease wall_thickness or increase alpha\n")
            f.write("  • If too flexible: increase wall_thickness or decrease alpha\n")
        
        print(f"📋 Generated: {info_file}")


def main():
    """Main function to generate auxetic sensor models."""
    
    print("🔬 Auxetic Capacitive Sensor - 3D Model Generator")
    print("=" * 60)
    
    # Create different sensor configurations
    configurations = [
        {
            "name": "Standard Sensor",
            "cell_size": 10.0,
            "wall_thickness": 1.0, 
            "alpha": 45.0,
            "nx": 3,
            "ny": 3,
            "suffix": "standard"
        },
        {
            "name": "High Sensitivity",
            "cell_size": 8.0,
            "wall_thickness": 0.8,
            "alpha": 60.0, 
            "nx": 4,
            "ny": 4,
            "suffix": "high_sens"
        },
        {
            "name": "Robust Design",
            "cell_size": 12.0,
            "wall_thickness": 1.5,
            "alpha": 30.0,
            "nx": 2, 
            "ny": 2,
            "suffix": "robust"
        }
    ]
    
    for config in configurations:
        print(f"\n🏗️  Generating {config['name']}...")
        
        sensor = AuxeticSensor3D(
            cell_size=config["cell_size"],
            wall_thickness=config["wall_thickness"],
            alpha=config["alpha"],
            nx=config["nx"],
            ny=config["ny"]
        )
        
        # Create output directory
        output_dir = f"cad/models_{config['suffix']}"
        
        try:
            step_file, stl_file, unit_file = sensor.export_models(output_dir)
            print(f"✅ {config['name']} completed successfully!")
            
        except Exception as e:
            print(f"❌ Error generating {config['name']}: {e}")
    
    print(f"\n🎉 All models generated!")
    print(f"📁 Check the cad/ directory for output files")
    print(f"🖨️  STL files are ready for 3D printing")
    print(f"🔧 STEP files can be opened in CAD software for modification")


if __name__ == "__main__":
    main() 