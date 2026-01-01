# NACA 4-Digit Airfoil Generator

This module provides a Python implementation of the classical **NACA 4-digit airfoil geometry**, enabling:

- Computation of airfoil coordinates from analytical definitions
- Visualization of the airfoil profile
- Generation of a 3D extruded solid
- Export to STL format for CFD meshing or CAD workflows

The implementation is intended for aerodynamic preprocessing within the context of
CFD simulations and surrogate modeling of wind turbine blade sections.

---

## Implemented Airfoil Definition

The airfoil geometry follows the standard NACA 4-digit formulation:

- **M**: maximum camber (first digit, % of chord)
- **P**: position of maximum camber (second digit, tenths of chord)
- **T**: maximum thickness (last two digits, % of chord)

Example:  
`NACA 2412` → M = 2%, P = 0.4, T = 12%

Both **closed** and **open trailing edge** configurations are supported.

---

## Usage Example

```python
from naca4_airfoil import NACA4Airfoil

airfoil = NACA4Airfoil.from_code("2412", closed_te=True)

# Plot airfoil geometry
airfoil.plot(step=0.01)

# Export extruded STL geometry
airfoil.export_stl(
    filename="naca2412.stl",
    step=0.005,
    thickness=1.0
)
