# CadQuery Installation Guide

This guide helps you install CadQuery for 3D model generation of the auxetic capacitive sensor.

## 🚀 Quick Installation (Recommended)

### Method 1: Using pip (Latest)
```bash
pip install cadquery-ocp
```

### Method 2: Using conda (Most Stable)
```bash
conda install -c conda-forge cadquery
```

## 🔧 Platform-Specific Instructions

### macOS
```bash
# Install via pip (recommended)
pip install cadquery-ocp

# Alternative: Using Homebrew + conda
brew install miniconda
conda install -c conda-forge cadquery
```

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# Install CadQuery
pip install cadquery-ocp

# If you get OpenGL errors:
sudo apt-get install python3-opengl
```

### Windows
```bash
# Using pip (in Command Prompt or PowerShell)
pip install cadquery-ocp

# Alternative: Using Anaconda
conda install -c conda-forge cadquery
```

## 🧪 Test Installation

After installation, test that CadQuery works:

```python
# test_cadquery.py
import cadquery as cq

# Create a simple box
box = cq.Workplane("XY").box(10, 10, 10)
print("✅ CadQuery installed successfully!")
print(f"Box volume: {box.val().Volume()}")
```

Run the test:
```bash
python -c "import cadquery as cq; print('✅ CadQuery works!')"
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Error: "No module named 'cadquery'"
```bash
# Make sure you're in the right environment
which python
pip list | grep cadquery

# Reinstall if needed
pip uninstall cadquery cadquery-ocp
pip install cadquery-ocp
```

#### 2. OpenCASCADE Errors
```bash
# Try the alternative OpenCASCADE package
pip uninstall cadquery-ocp
pip install opencascade-python
pip install cadquery
```

#### 3. macOS: "Symbol not found" errors
```bash
# Install via conda instead
conda install -c conda-forge cadquery
```

#### 4. Linux: Missing system libraries
```bash
# Install required system packages
sudo apt-get install libgl1-mesa-glx libglib2.0-0 libxrender1 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

#### 5. Windows: Visual C++ errors
- Install Microsoft Visual C++ Redistributable
- Or use Anaconda distribution instead of pip

### Alternative: Docker Installation

If you're having persistent issues, use Docker:

```dockerfile
# Dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install cadquery-ocp numpy matplotlib

WORKDIR /app
COPY . .

CMD ["python", "cad/auxetic_cell_3d.py"]
```

Build and run:
```bash
docker build -t auxetic-sensor .
docker run -v $(pwd)/cad:/app/cad auxetic-sensor
```

## 📦 Alternative CAD Solutions

If CadQuery installation fails, consider these alternatives:

### 1. FreeCAD Python API
```bash
# Install FreeCAD
# macOS: brew install freecad
# Linux: sudo apt-get install freecad
# Windows: Download from freecad.org

# Use FreeCAD's Python API (more complex but very powerful)
```

### 2. OpenSCAD + Python
```bash
pip install solidpython2

# Generate OpenSCAD code from Python
# Then use OpenSCAD GUI to export STL
```

### 3. Fusion 360 Python API
- Requires Fusion 360 license (free for personal use)
- More complex setup but very powerful
- Good for complex assemblies

### 4. Online CAD (Recommended if local install fails)
- **OnShape**: Free online CAD with Python API
- **Tinkercad**: Simple browser-based CAD
- **Fusion 360 Online**: Web-based version

## 🎯 Recommended Workflow

1. **Try pip installation first**: `pip install cadquery-ocp`
2. **If that fails, try conda**: `conda install -c conda-forge cadquery`
3. **If still failing, use our test script**: `python cad/test_3d_model.py`
4. **For production, consider OnShape or Fusion 360**

## 📋 Verification Checklist

- [ ] CadQuery imports without errors
- [ ] Can create simple geometry (box, cylinder)
- [ ] Can export to STL format
- [ ] Our test script runs successfully: `python cad/test_3d_model.py`
- [ ] Main 3D generator works: `python cad/auxetic_cell_3d.py`

## 🆘 Still Having Issues?

1. **Check our test script first**: `python cad/test_3d_model.py`
   - This tests the geometry logic without requiring CadQuery
   
2. **Use the simulation instead**: `jupyter lab simulations/simulation.ipynb`
   - Provides 2D visualization and analysis
   
3. **Manual CAD approach**:
   - Use the geometry data from `src/design.py`
   - Import coordinates into your preferred CAD software
   - Manually create the 3D model

4. **Contact support**:
   - Create an issue with your error message
   - Include your OS, Python version, and installation method

## 🔗 Useful Links

- [CadQuery Documentation](https://cadquery.readthedocs.io/)
- [CadQuery GitHub](https://github.com/CadQuery/cadquery)
- [Installation Troubleshooting](https://cadquery.readthedocs.io/en/latest/installation.html)
- [CadQuery Examples](https://github.com/CadQuery/cadquery/tree/master/examples) 