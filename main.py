"""RUN THIS FILE - where all the key parameters are set"""

from typing import Tuple

from src.solver import DyeSolver2D
from src.rendering import Rendering
from src.plots import AnimatedPlots

# height * width (because numpy arrays are indexed in [row, column])
# for part 9:

# MESH_SHAPE: Tuple[int, int] = (7, 7) # small mesh
MESH_SHAPE: Tuple[int, int] = (21, 21) # medium mesh
# MESH_SHAPE: Tuple[int, int] = (301, 301) # stupidly large mesh (VERY SLOW)

# dimensions in mm - width * height in this case
# (because pygame works in (x, y) coords)
MESH_DIM = (80, 80)

# main entry point
if __name__ == "__main__":
    solver = DyeSolver2D(MESH_SHAPE, MESH_DIM)
    plotter = AnimatedPlots(solver, anim_length=15)

    # Pygame interactive animation (plot #1 AND really cool)
    renderer = Rendering(solver)
    renderer.run()
    
    # Matplotlib animation (plot #2)
    # plotter.run_dye_animation()

    # Velocity plot (plot #3)
    # plotter.run_velocity_animation()