# scripts/plot_airfoil.py

from geometry.naca4 import NACA4Airfoil
from geometry.plot import AirfoilPlotter
from geometry.transform import AirfoilTransform
from geometry.export_stl import AirfoilExporterSTL

def main():
    airfoil = NACA4Airfoil.from_code("2512")
    contour = airfoil.coordinates(step=0.01)
    AirfoilPlotter.plot_contour(contour, title="NACA")

    AirfoilPlotter.plot_contour(AirfoilTransform.rotate(contour, 45), title="NACA")
    AirfoilExporterSTL.export_from_contour(contour, "airfoil.stl")



if __name__ == "__main__":
    main()
