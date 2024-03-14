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
from src.resources import (
    border,
    textbox_width,
)

# suppress ALSA error (WSL2 error I think)
os.environ["SDL_AUDIODRIVER"] = "dsp"

# COMPUTER SCREEN SPECIFIC STUFF - SHOULDN'T NEED TOOOOO MUCH CHANGING
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DIAG_INCHES = 15.6
DIAG_MM = DIAG_INCHES * 25.4

# Pixels per mm
PPMM = math.sqrt(math.pow(SCREEN_WIDTH, 2) + math.pow(SCREEN_HEIGHT, 2)) / DIAG_MM

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Rendering:
    """Handles the main rendering loop and the rendering of the mesh"""

    MARGIN_X = 200
    MARGIN_Y = 40

    def __init__(
        self,
        solver: DyeSolver2D,
    ) -> None:
        self.solver = solver
        self.mesh_shape = solver.mesh_shape
        self.mesh_dim = solver.mesh_dim

        # dimensions needs to be integers because pygame
        # works in discrete pixels
        self.cell_dim: Tuple[int, int] = (
            round(self.mesh_dim[0] * PPMM / self.mesh_shape[1]),
            round(self.mesh_dim[1] * PPMM / self.mesh_shape[0]),
        )
        self.display_dim: Tuple[int, int] = (
            self.cell_dim[0] * self.mesh_shape[1],
            self.cell_dim[1] * self.mesh_shape[0],
        )

        self.gui_dim: Tuple[int, int] = (
            self.display_dim[0] + 2 * self.MARGIN_X,
            self.display_dim[1] + 2 * self.MARGIN_Y,
        )
        self.mesh_pos: Tuple[int, int] = (self.MARGIN_X, self.MARGIN_Y)

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.gui_dim)
        self.running = True

    def run(self) -> None:
        while self.running:
            self.screen.fill(WHITE)
            self.__handle_events()

            # time since last call - for unsteady term
            dt = self.clock.tick()

            # update the velocity then solve the problem
            self.solver.sinusoidal_velocity(pygame.time.get_ticks())
            self.solver.solve(dt / 1000)
            self.__paint_mesh()

            textbox_width(
                self.screen,
                (self.gui_dim[0] - self.MARGIN_X + 20, self.MARGIN_Y),
                self.MARGIN_X - 25,
                "Velocity: ZDFSD\nStuff: thing",
            )

            # paint all changes to the display
            pygame.display.flip()

        # once running != True, quit
        pygame.quit()

    def __paint_mesh(self) -> None:
        # loop through all the cells and paint them black proportional
        # to the dye concentration at each mesh
        mesh = pygame.Surface(self.display_dim)

        for i in range(self.mesh_shape[0]):
            for j in range(self.mesh_shape[1]):
                color: int = round(255 - self.solver.mesh[i, j] * 2.55)
                if color > 255:
                    color = 255
                mesh.fill(
                    (color, color, color),
                    rect=(
                        (j * self.cell_dim[0], i * self.cell_dim[1]),
                        self.cell_dim,
                    ),
                )
        self.screen.blit(mesh, self.mesh_pos)
        border(
            self.screen,
            self.mesh_pos,
            self.display_dim,
            "MESH ANIMATION",
        )

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.type == QUIT:
                    self.running = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                mesh_i = math.floor((pos[1] - self.MARGIN_Y) / self.cell_dim[1])
                mesh_j = math.floor((pos[0] - self.MARGIN_X) / self.cell_dim[0])
                if (
                    mesh_i < self.solver.mh
                    and mesh_j < self.solver.mw
                    and mesh_i >= 0
                    and mesh_j >= 0
                ):
                    self.solver.mesh[mesh_i, mesh_j] = 100

        # test to see if mouse button is currently pressed down to
        # enable holding and dragging :)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            mesh_i = math.floor((pos[1] - self.MARGIN_Y) / self.cell_dim[1])
            mesh_j = math.floor((pos[0] - self.MARGIN_X) / self.cell_dim[0])
            if (
                mesh_i < self.solver.mh
                and mesh_j < self.solver.mw
                and mesh_i >= 0
                and mesh_j >= 0
            ):
                self.solver.mesh[mesh_i, mesh_j] = 100
