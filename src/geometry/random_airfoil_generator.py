from geometry.naca4 import NACA4Airfoil
from geometry.transform import AirfoilTransform
from geometry.export_stl import export_from_contour

from pathlib import Path
import numpy as np
import random
import shutil


def random_airfoil(
    M_range=(0, 9),
    P_range=(1, 9),
    T_range=(6, 18),
    closed_te=True,
    seed=None,
) -> NACA4Airfoil:
    """
    Generate a random NACA 4-digit airfoil within realistic bounds.

    Parameters
    ----------
    M_range : tuple[int, int]
        Range for maximum camber (percent).
    P_range : tuple[int, int]
        Range for camber position (tenths of chord).
    T_range : tuple[int, int]
        Range for thickness (percent).
    closed_te : bool
        Whether the trailing edge is closed.
    seed : int | None
        Random seed for reproducibility.

    Returns
    -------
    NACA4Airfoil
        Randomly generated airfoil.
    """

    if seed is not None:
        random.seed(seed)

    M = random.randint(*M_range)
    P = random.randint(*P_range)
    T = random.randint(*T_range)

    return NACA4Airfoil(M, P, T, closed_te=closed_te)


def generator(
    N: int,
    angles,
    base: str | Path,
    origin: str | Path,
):
    """
    Generate random airfoils, rotate them by given angles,
    and export STL files into simulation folders.

    Parameters
    ----------
    N : int
        Number of random airfoils to generate.
    angles : iterable of float
        Rotation angles in degrees.
    base : str | Path
        Base directory where simulations will be created.
    origin : str | Path
        Template directory to be copied into each simulation folder.
    """

    base = Path(base).resolve()
    origin = Path(origin).resolve()

    if not origin.exists():
        raise FileNotFoundError(f"Origin directory does not exist: {origin}")

    base.mkdir(parents=True, exist_ok=True)

    counter = 0

    for _ in range(N):
        airfoil = random_airfoil()

        for angle in angles:
            counter += 1

            simulation_name = f"motorbike_{counter:04d}"
            simulation_path = base / simulation_name
            airfoil_path=simulation_path/"constant"/"triSurface"


            # Copy template directory
            shutil.copytree(origin, simulation_path)

            # Generate rotated airfoil contour
            contour = AirfoilTransform.rotate(
                airfoil.coordinates(step=0.01),
                angle
            )

            # Export STL inside the simulation folder
            export_from_contour(
                contour=contour,
                filename="op1.stl",
                output_dir=airfoil_path
            )




