import numpy as np
import cadquery as cq
from cadquery import exporters

class AirfoilExporterSTL:
    """Exports a 2D airfoil contour (Nx2) to an STL by extrusion using CadQuery."""

    @staticmethod
    def export_from_contour(
        contour: np.ndarray,
        filename: str,
        thickness: float = 0.5,
        workplane: str = "XY",
        ensure_closed: bool = True
    ) -> None:
        """
        Export an STL from a 2D contour by extruding it.

        Parameters
        ----------
        contour : np.ndarray
            Nx2 array of [x, y] points describing the airfoil contour.
            Points should define a non-self-intersecting loop.
        filename : str
            Output STL file name (e.g., "naca2412.stl").
        thickness : float
            Extrusion thickness (in the same units as your points, usually mm).
        workplane : str
            CadQuery workplane (default "XY").
        ensure_closed : bool
            If True, closes the polyline before extrusion.
        """
        pts = np.asarray(contour, dtype=float)

        if pts.ndim != 2 or pts.shape[1] != 2:
            raise ValueError("contour must be an Nx2 array")

        if len(pts) < 3:
            raise ValueError("contour must contain at least 3 points")

        if thickness <= 0:
            raise ValueError("thickness must be > 0")

        # CadQuery expects Python tuples/lists of (x, y)
        pts_list = [(float(x), float(y)) for x, y in pts]

        wp = cq.Workplane(workplane).polyline(pts_list)

        if ensure_closed:
            wp = wp.close()

        # Extrude the closed wire to form a solid
        solid = wp.extrude(thickness)

        # Export STL
        exporters.export(solid, filename)

