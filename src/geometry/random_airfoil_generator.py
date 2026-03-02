from geometry.naca4 import NACA4Airfoil
from geometry.transform import AirfoilTransform
from geometry.export_stl import export_from_contour
from geometry.sdf import compute_sdf
import pandas as pd
from pathlib import Path
import numpy as np
import random
import shutil
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def random_airfoil(
    M_range=(0, 6),
    P_range=(2, 8),
    T_range=(8, 24),
    closed_te=True,
    seed=None,
) -> NACA4Airfoil:
    """
    Generate a random NACA 4-digit airfoil within stable bounds for SDF/grid pipelines.

    Parameters
    ----------
    M_range : tuple[int, int]
        Range for maximum camber digit (0–6). Capped at 6 to avoid extreme camber.
    P_range : tuple[int, int]
        Range for camber-position digit (2–8). When M > 0, values below 2 place
        the camber peak too close to the leading edge and cause discretisation
        artefacts on 512×256 grids.
    T_range : tuple[int, int]
        Range for thickness digits (8–24). Thinner profiles (< 8 %) are too thin
        to resolve accurately on a 200×80 sub-grid.
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
    # When cambered, keep camber peak away from the leading edge (P >= 2)
    P_min = max(P_range[0], 2) if M > 0 else P_range[0]
    P = random.randint(P_min, P_range[1])
    T = random.randint(*T_range)

    return NACA4Airfoil(M, P, T, closed_te=closed_te)


def _save_sdf_image(
    sdf: np.ndarray,
    airfoil: NACA4Airfoil,
    angle: float,
    output_dir: Path,
) -> None:
    """Save a PNG of the SDF field to *output_dir*."""
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 0.5

    label = f"NACA {airfoil.M_digit}{airfoil.P_digit}{airfoil.T_digits:02d}"

    fig = Figure(figsize=(8, 3))
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)

    im = ax.imshow(
        sdf,
        origin="lower",
        extent=[x_min, x_max, y_min, y_max],
        cmap="viridis",
        aspect="auto",
        interpolation="bilinear",
    )
    fig.colorbar(im, ax=ax, label="Signed distance")

    ax.set_title(f"SDF — {label}  |  α = {angle:.1f}°", fontsize=11, fontweight="bold")
    ax.set_xlabel("x / c", fontsize=9)
    ax.set_ylabel("y / c", fontsize=9)

    fig.tight_layout()
    code = f"{airfoil.M_digit}{airfoil.P_digit}{airfoil.T_digits:02d}"
    filename = f"sdf_NACA_{code}_{angle:.1f}deg.png".replace(" ", "")
    fig.savefig(output_dir / filename, dpi=150)


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

    #  SDF initialization
    sdf_df = pd.DataFrame(columns=['SDF','Simulation'])

    for i in range(N):
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

            # Compute SDF with cosine-spaced contour for better leading-edge resolution
            contour_sdf = AirfoilTransform.rotate(
                airfoil.coordinates_cosine(n_points=500),
                angle
            )
            sdf=compute_sdf(contour_sdf)
            _save_sdf_image(sdf, airfoil, angle, airfoil_path)

            sdf_df.loc[counter,"Simulation"]=simulation_name
            sdf_df.loc[counter, 'SDF'] = sdf

            # Export STL inside the simulation folder
            export_from_contour(
                contour=contour,
                filename="op1.stl",
                output_dir=airfoil_path
            )
    # Export dataframe SDF
    sdf_df.to_pickle(base/"sdf_df.pkl")




