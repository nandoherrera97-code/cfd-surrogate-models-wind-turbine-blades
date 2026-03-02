import numpy as np
from scipy.spatial import KDTree
from matplotlib.path import Path as MplPath


def compute_sdf(
    contour,
    airfoil_step: float = 0.002,
    # ------------ flujo paralelo ------------
    x_min: float = -0.5,
    x_max: float = 1.5,
    y_min: float = -0.5,
    y_max: float = 0.5,
    resolution_x: int = 512,
    resolution_y: int = 256,
    signed_distance: bool = True,
):
    """
    Compute a 2D Signed Distance Function (SDF) of the airfoil.

    Returns
    -------
    sdf : ndarray (resolution_y, resolution_x)
        Signed distance field.
    """
    xs = np.linspace(x_min, x_max, resolution_x)
    ys = np.linspace(y_min, y_max, resolution_y)
    X, Y = np.meshgrid(xs, ys)

    query_points = np.column_stack([X.ravel(), Y.ravel()])

    # Fast nearest-neighbour distance via KDTree
    tree = KDTree(contour)
    distances, _ = tree.query(query_points)
    sdf = distances.reshape(resolution_y, resolution_x)

    # Vectorised inside/outside test
    path = MplPath(contour)
    inside_mask = path.contains_points(query_points).reshape(resolution_y, resolution_x)

    if signed_distance:
        sdf[inside_mask] = -1.0

    sdf = np.flipud(sdf)
    return sdf
