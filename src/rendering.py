"""
Pygame rendering loop and mesh rendering stored in an object

Should have a main method "run" which starts the pygame rendering loop,
also the main rendering surface and key reference dimensions are
computed and stored here.

Also should handle events and mouse input for manual addition of dye
to the mesh.
"""

import math
from typing import Tuple
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)
import os

from src.solver import DyeSolver2D

# suppress ALSA error (WSL2 error I think)
os.environ["SDL_AUDIODRIVER"] = "dsp"

# COMPUTER SCREEN SPECIFIC STUFF - SHOULDN'T NEED TOOOOO MUCH CHANGING
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DIAG_INCHES = 15.6
DIAG_MM = DIAG_INCHES * 25.4

# Pixels per mm
PPMM = math.sqrt(math.pow(SCREEN_WIDTH, 2) + math.pow(SCREEN_HEIGHT, 2)) / DIAG_MM


class Rendering:
    """Handles the main rendering loop and the rendering of the mesh"""

    def __init__(
        self,
        solver: DyeSolver2D,
    ) -> None:
        self.solver = solver
        self.mesh_shape = solver.mesh_shape
        self.mesh_dim = solver.mesh_dim

        # dimensions needs to be integers because pygame
        # works in discrete pixels
        self.display_dim: Tuple[int, int] = (
            round(self.mesh_dim[0] * PPMM),
            round(self.mesh_dim[1] * PPMM),
        )
        self.cell_dim: Tuple[int, int] = (
            round(self.display_dim[0] / self.mesh_shape[1]),
            round(self.display_dim[1] / self.mesh_shape[0]),
        )

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.display_dim)

    def run(self) -> None:
        self.screen.fill((255, 255, 255))
        running = True

        while running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.type == QUIT:
                        running = False

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    mesh_i = math.floor(pos[1] / self.cell_dim[1])
                    mesh_j = math.floor(pos[0] / self.cell_dim[0])
                    self.solver.mesh[mesh_i, mesh_j] = 100

            # test to see if mouse button is currently pressed down to
            # enable holding and dragging :)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                self.solver.mesh[
                    math.floor(pos[1] / self.cell_dim[1]),
                    math.floor(pos[0] / self.cell_dim[0]),
                ] = 100

            # time since last call - for unsteady term
            dt = self.clock.tick()

            # loop through all the cells and paint them black proportional
            # to the dye concentration at each mesh
            for i in range(self.mesh_shape[0]):
                for j in range(self.mesh_shape[1]):
                    color: int = round(255 - self.solver.mesh[i, j] * 2.55)
                    if color > 255:
                        color = 255
                    self.screen.fill(
                        (color, color, color),
                        rect=(
                            (j * self.cell_dim[0], i * self.cell_dim[1]),
                            self.cell_dim,
                        ),
                    )

            # update velocity with the sinusoidal function
            self.solver.sinusoidal_velocity(pygame.time.get_ticks())

            # actually solve the problem for the next time round
            self.solver.solve(dt / 1000)

            # push all the display changes to the screen
            pygame.display.flip()

        # once running != True, quit
        pygame.quit()
