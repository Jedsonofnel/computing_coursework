"""
Object for creating animations
"""

from src.solver import DyeSolver2D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AnimatedPlots:
    FPS = 30

    def __init__(self, solver: DyeSolver2D, anim_length: int = 100) -> None:
        self.solver = solver
        self.length = anim_length

        self.num_frames: int = self.FPS * self.length
        self.time_step: float = 1 / self.FPS * 1000 # in ms

        self.dye_data = np.zeros((self.num_frames, self.solver.mh, self.solver.mw))

        # where are all the centroids positioned; (0, 0) is bottom left
        x_values = np.arange(
            self.solver.cw / 2, self.solver.mw * self.solver.cw, self.solver.cw
        )
        y_values = np.arange(
            self.solver.ch / 2, self.solver.mh * self.solver.ch, self.solver.ch
        )

        self.x_pos, self.y_pos = np.meshgrid(x_values, y_values, indexing="xy")

    def run_dye_animation(self) -> None:
        print(f"CALCULATING DYE DISTRIBUTION OVER {self.length} SECONDS")
        print("may take a few moments...")

        for frame in range(self.num_frames):
            self.solver.sinusoidal_velocity((frame + 1) * self.time_step)
            self.dye_data[frame] = self.solver.solve(self.time_step / 1000)

        fig, ax = plt.subplots()
        colormesh = ax.pcolormesh(self.x_pos, self.y_pos, self.dye_data[0], cmap="plasma")

        def update(frame):
            frame_data = self.dye_data[frame]
            colormesh.set_array(frame_data.ravel())
            return colormesh

        ani = animation.FuncAnimation(
            fig=fig, func=update, frames=self.num_frames, interval=self.time_step
        )
        ax.set_title("Dye Concentration Plot In Water Flow")
        ax.set_aspect(1)
        ax.set_xlabel("Position [mm]")
        ax.set_ylabel("Position [mm]")
        fig.colorbar(colormesh, ax=ax)

        plt.show()

    def run_velocity_animation(self) -> None:
        velocities = np.zeros((self.num_frames, 2))

        for frame in range(self.num_frames):
            self.solver.sinusoidal_velocity((frame + 1) * self.time_step)
            velocities[frame, 1] = self.solver.velocity_magnitude()
            velocities[frame, 0] = self.solver.velocity_theta()

        fig = plt.figure(figsize=(6,6))
        ax = plt.subplot(111, polar=True)

        line, = ax.plot([],[])
        ax.set_ylim((0, 0.2))
        ax.set_yticks([0.05, 0.10, 0.15, 0.20])
        ax.set_ylabel("Magnitude")

        ax.set_title("Fluid Velocity Function Display")

        def update(frame):
            line.set_xdata([0, velocities[frame, 0]])
            line.set_ydata([0, velocities[frame, 1]])
            return line
        
        ani = animation.FuncAnimation(
            fig=fig, func=update,frames=self.num_frames, interval=self.time_step
        )



        plt.show()