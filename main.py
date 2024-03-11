"""RUN THIS FILE - where all the key parameters are set"""

from typing import Tuple

from src.solver import DyeSolver2D
from src.rendering import Rendering

# height * width (because numpy arrays are indexed in [row, column])
MESH_SHAPE: Tuple[int, int] = (21, 21)

# dimensions in mm - width * height in this case
# (because pygame works in (x, y) coords)
MESH_DIM = (100, 100)

# main entry point
if __name__ == "__main__":
    solver = DyeSolver2D(MESH_SHAPE, MESH_DIM)
    renderer = Rendering(solver)

    renderer.run()
