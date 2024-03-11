"""
Dye Solver Object defined here

Stores the mesh object and other paramaters, has a main method "solve"
which runs an iteration of the solver over a time "dt" and returns
the mesh in its state after the iteration.
"""

import math
from typing import Tuple

import numpy as np
import numpy.typing as npt


class DyeSolver2D:
    DENSITY = 2.55
    DIFFUSIVITY = 1e-4

    def __init__(
        self,
        mesh_shape: Tuple[int, int],
        mesh_dim: Tuple[int, int],
        flow_velocity: Tuple[float, float] = (0.1, 0),
    ):
        self.mesh_shape = mesh_shape
        self.mesh_dim = mesh_dim

        # mesh width and height
        # numpy shape = (rows, columns)
        self.mh = mesh_shape[0]
        self.mw = mesh_shape[1]

        # the MESH - initially no dye anywhere
        self.mesh: npt.NDArray = np.zeros(mesh_shape)

        # num of cells
        self.num = self.mw * self.mh

        # system of coefficients for every cell in the mesh
        # cell with index [i, j] will have index [i * mw + j, i * mw + j]
        self.system: npt.NDArray = np.zeros((self.num, self.num))
        self.b: npt.NDArray = np.zeros((self.num, 1))

        # cell width and height
        # make sure to convert mesh dimensions to m
        self.cw = (mesh_dim[0] / 1000) / self.mw
        self.ch = (mesh_dim[1] / 1000) / self.mh

        # set middle (or closest to middle) cell to 100% dye concentration
        self.source_cell: Tuple[int, int] = (
            math.floor(self.mh / 2),
            math.floor(self.mw / 2),
        )
        self.mesh[self.source_cell] = 100

        self.flow_velocity = flow_velocity

    def __get_index(self, i: int, j: int) -> int:
        """Gets the system index of a cell with mesh index [i, j]"""
        return i * self.mw + j

    def solve(self, dt: float = 0) -> npt.NDArray:
        # update coefficients in system
        for i in range(self.mh):
            for j in range(self.mw):
                sys_index = self.__get_index(i, j)

                # f is mass flow rate
                f_x: float = self.DENSITY * self.flow_velocity[0] * self.ch
                f_y: float = self.DENSITY * self.flow_velocity[1] * self.cw
                d_x: float = self.DIFFUSIVITY * self.ch / self.cw
                d_y: float = self.DIFFUSIVITY * self.cw / self.ch

                # using upwind differencing
                a_e: float = d_x + max(-f_x, 0)
                a_w: float = d_x + max(f_x, 0)
                a_n: float = d_y + max(-f_y, 0)
                a_s: float = d_y + max(f_y, 0)

                # dirichlet boundary conditions: concentration at 0
                # 0 is default - only change if not at boundary
                if j != self.mw - 1:
                    self.system[sys_index, sys_index + 1] = -a_e

                if j != 0:
                    self.system[sys_index, sys_index - 1] = -a_w

                if i != self.mh - 1:
                    self.system[sys_index, self.__get_index(i + 1, j)] = -a_n

                if i != 0:
                    self.system[sys_index, self.__get_index(i - 1, j)] = -a_s

                a_p_0: float
                if dt == 0:
                    a_p_0 = 1000000  # very large
                else:
                    a_p_0 = self.DENSITY * self.cw * self.ch / dt

                self.system[sys_index, sys_index] = a_e + a_w + a_n + a_s + a_p_0

                self.b[sys_index, 0] = a_p_0 * self.mesh[i, j]

                # solve
        solution = np.linalg.solve(self.system, self.b)

        # use solution to update mesh
        self.mesh = np.reshape(solution, (self.mesh.shape))

        # set dye source to constant concentration
        self.mesh[self.source_cell] = 100

        return self.mesh

    def sinusoidal_velocity(self, time_ms: float) -> None:
        time = time_ms / 1000
        x_velocity = 0.15 * math.sin(time * 2 * math.pi / 23)
        y_velocity = 0.1 * math.sin(time * 2 * math.pi / 10 + 3)
        self.flow_velocity = (x_velocity, y_velocity)
