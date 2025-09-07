# Capacitive Auxetic Sensor Development Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Environment Setup
```bash
# Create isolated Python environment - NEVER CANCEL: Takes 5 minutes for dependency downloads
python -m venv env
source env/bin/activate
pip install -r requirements.txt  # NEVER CANCEL: 3-5 minutes, timeout 600+ seconds

# CRITICAL: pip install often fails due to network limitations in sandboxed environments
# If pip install fails with "Read timed out" or similar network errors:
# 1. This is EXPECTED and NORMAL in restricted network environments
# 2. Try installing core packages only: pip install numpy matplotlib scipy pytest
# 3. Some functionality may be limited but core algorithms still work
# 4. Document in instructions: "Network limitations prevent full dependency installation"
```

### Core Development Workflow
```bash
# ALWAYS run these validation steps after making changes:
source env/bin/activate  # Always activate environment first

# Primary validation (requires dependencies):
python demo.py           # Fast validation: <5 seconds (if deps available)
pytest                   # Test suite: ~2 seconds, timeout 60 seconds (if deps available)
python cad/test_3d_model.py  # 3D model logic test: <5 seconds (if deps available)

# Alternative validation (works without full dependencies):
python3 -m py_compile src/*.py  # Syntax check: <1 second per file
python3 -c "import src.design; print('Core imports work')"  # Import test: <1 second
find . -name "*.py" -not -path "./.deps/*" -not -path "./env/*" | xargs python3 -m py_compile  # All files: <5 seconds
```

### 3D Model Generation
```bash
# Test 3D model logic (works without CadQuery installation):
python cad/test_3d_model.py

# Actual 3D model generation (requires CadQuery):
# WARNING: CadQuery installation often fails due to network/dependency issues
pip install cadquery  # May fail - see troubleshooting below
python cad/auxetic_cell_3d.py  # Generates STL/STEP files if CadQuery works
```

### Code Quality Validation
```bash
# ALWAYS run before committing - CI will fail without these:
black --exclude='\.deps|env' src/ cad/ tests/ demo.py  # Format code
flake8 --exclude='.deps,env' src/ cad/ tests/ demo.py  # Check style

# WARNING: Current codebase has formatting issues that need fixing
# Black will reformat 10 files, flake8 shows many style violations
# Fix these before making changes to avoid masking your modifications
```

### Notebook Development
```bash
# Run Jupyter for simulation analysis:
jupyter lab simulations/simulation.ipynb  # Interactive analysis environment
```

## Validation Scenarios

### CRITICAL: Manual Testing Requirements
After making changes to the codebase, ALWAYS run these complete scenarios:

#### 1. Core Functionality Test (Full Dependencies Required)
```bash
source env/bin/activate
python demo.py
```
**Expected Output**: Should show auxetic cell designs with different angles (30°, 45°, 60°), Poisson ratios, and complete without errors.
**Fallback**: If dependencies missing, see Alternative Validation below.

#### 2. Algorithm Validation Test (Full Dependencies Required)
```bash
source env/bin/activate
pytest tests/test_design.py -v
```
**Expected Output**: All design function tests should pass, validating cell geometry generation and Poisson ratio calculations.
**Fallback**: If pytest unavailable, use syntax checking below.

#### 3. 3D Model Generation Test (Works Without Dependencies)
```bash
source env/bin/activate
python cad/test_3d_model.py
```
**Expected Output**: Should simulate 3D model generation steps and show file outputs (auxetic_sensor.stl, etc.) without requiring CadQuery.
**Fallback**: Check syntax with `python3 -m py_compile cad/test_3d_model.py`

#### 4. Alternative Validation (No Dependencies Required)
```bash
# Syntax validation for all Python files:
find . -name "*.py" -not -path "./.deps/*" -not -path "./env/*" | xargs python3 -m py_compile

# Core module import test:
python3 -c "import src.design as design; print('✅ Core design module syntax OK')"
python3 -c "import src.utils as utils; print('✅ Utils module syntax OK')"
python3 -c "import src.test_setup as test_setup; print('✅ Test setup module syntax OK')"

# Basic algorithm test (no numpy required):
python3 -c "import math; print('✅ Basic math:', math.sqrt(16))"
```
**Expected Output**: All files should compile without syntax errors, imports should succeed.

## Troubleshooting and Known Issues

### CadQuery Installation Problems
**COMMON ISSUE**: `pip install cadquery` frequently fails with network timeouts or dependency conflicts.

**Workarounds**:
1. Use test simulation instead: `python cad/test_3d_model.py`
2. cadquery-ocp is already installed but import fails - this is normal
3. For actual 3D generation, document in instructions: "CadQuery installation fails due to network limitations"

### Code Formatting Issues  
**CURRENT STATE**: Codebase has significant formatting violations:
- Black wants to reformat 10 files
- Flake8 shows 200+ style violations (whitespace, line length, imports)

**Resolution**: Run black and fix flake8 issues before making changes to avoid confusion about what changed.

### Network/Dependency Limitations
**CRITICAL ISSUE**: Package installation frequently fails in sandboxed environments:
- `pip install -r requirements.txt` often times out with "Read timed out" errors
- This is EXPECTED behavior in restricted network environments  
- Core Python functionality works but scientific packages may be unavailable
- CadQuery installation almost always fails
- Some validation steps will not work without full dependencies

**Workarounds**:
1. Document installation failures as expected: "pip install fails due to network limitations"
2. Use system Python packages when available
3. Focus on code structure and logic validation rather than full functionality tests
4. Prioritize tasks that don't require heavy dependencies

## Timing Expectations and Timeouts

**NEVER CANCEL** these operations - use these timeout values:

| Operation | Expected Time | Timeout Setting |
|-----------|---------------|-----------------|
| `pip install -r requirements.txt` | 3-5 minutes (often fails) | 600+ seconds |
| `python demo.py` | <5 seconds | 30 seconds |
| `pytest` | ~2 seconds | 60 seconds |
| `python cad/test_3d_model.py` | <5 seconds | 30 seconds |
| `python3 -m py_compile *.py` | <1 second per file | 30 seconds |
| `find + py_compile all files` | <5 seconds total | 30 seconds |
| `black` formatting | <10 seconds | 60 seconds |
| `flake8` checking | <15 seconds | 60 seconds |
| `jupyter lab` startup | <30 seconds | 60 seconds |

## Repository Structure Reference

```
.
├── README.md                    # Project overview and quickstart
├── requirements.txt             # Python dependencies
├── demo.py                      # Complete demonstration script
├── src/
│   ├── design.py               # Core auxetic cell design functions
│   ├── utils.py                # Mathematical utilities  
│   └── test_setup.py           # Measurement system simulation
├── cad/
│   ├── auxetic_cell_3d.py      # 3D model generator (requires CadQuery)
│   ├── test_3d_model.py        # Test 3D logic without CadQuery
│   └── INSTALL_CADQUERY.md     # CadQuery installation guide
├── tests/
│   ├── test_design.py          # Design function tests
│   ├── test_utils.py           # Utility function tests
│   └── test_test_setup.py      # Measurement system tests
├── simulations/
│   └── simulation.ipynb        # Jupyter analysis notebook
└── docs/
    └── project_outline.md      # Project phases and goals
```

## Key Design Concepts

### Auxetic Structures
- **Re-entrant geometry**: Negative Poisson's ratio materials
- **Key angles**: 30° (conservative), 45° (balanced), 60° (aggressive)
- **Poisson ratios**: All designs should show negative values (auxetic behavior)

### Capacitive Sensing
- **Principle**: Capacitance changes with mechanical deformation
- **Simulation**: MockLCRMeter class provides realistic noise and drift
- **Analysis**: Moving average filtering and calibration curves

### 3D Manufacturing
- **Output formats**: STL (3D printing), STEP (CAD editing)  
- **Configurations**: Standard, High Sensitivity, Robust variants
- **Integration**: Uses core design functions for mathematical accuracy

## Common Development Tasks

### Adding New Auxetic Designs
1. Modify `src/design.py` - `generate_reentrant_cell()` function
2. Run `python demo.py` to validate geometry
3. Run `pytest tests/test_design.py` to check calculations
4. Update `cad/auxetic_cell_3d.py` if 3D model changes needed

### Modifying Simulation Parameters
1. Edit `src/test_setup.py` - MockLCRMeter class
2. Run `pytest tests/test_test_setup.py` to validate
3. Test integration with `python demo.py`

### Updating Analysis Functions
1. Modify `src/utils.py` functions
2. Run `pytest tests/test_utils.py` to verify
3. Check notebook compatibility: `jupyter lab simulations/simulation.ipynb`

## NEVER DO These Things
- Do not try to install additional CAD software - use the Python-based tools
- Do not cancel long-running pip installs - network delays are normal
- Do not skip the formatting fixes - they will mask your actual changes
- Do not modify files in `.deps/` directory - these are pytest internals
- Do not commit the `env/` virtual environment directory

## Build/CI Validation
No formal CI pipeline exists, but follow this checklist before considering changes complete:

### Full Validation (If Dependencies Available)
- [ ] `python demo.py` runs successfully and shows auxetic designs
- [ ] `pytest` shows all tests passing (~23 tests expected)  
- [ ] `python cad/test_3d_model.py` completes without errors
- [ ] `black` and `flake8` pass (after fixing existing issues)
- [ ] Virtual environment can be recreated from scratch

### Alternative Validation (Always Available)
- [ ] `find . -name "*.py" -not -path "./.deps/*" -not -path "./env/*" | xargs python3 -m py_compile` succeeds
- [ ] `python3 -c "import src.design; import src.utils; import src.test_setup; print('All core modules OK')"` succeeds
- [ ] File structure is intact (11 Python files expected in project)
- [ ] No syntax errors in any Python files

### Validation Command Reference
```bash
# Quick syntax validation (no dependencies):
python3 -m py_compile src/*.py tests/*.py cad/*.py demo.py

# Core module validation:
python3 -c "import src.design as d; import src.utils as u; import src.test_setup as t; print('Core OK')"

# File count check:
find . -name "*.py" -not -path "./.deps/*" -not -path "./env/*" | wc -l  # Should show 11

# Environment setup validation:
python3 -m venv test_env && echo "Virtual environment creation works"
```

## Performance Notes
- **Memory usage**: Scientific computing packages require ~500MB RAM
- **Disk space**: Virtual environment uses ~200MB
- **CPU usage**: All operations are compute-light, no heavy numerical processing
- **Network**: Initial setup requires reliable internet for package downloads