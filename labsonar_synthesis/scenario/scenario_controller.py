"""
Scenario Controller Module

This module contains the ScenarioController class, designed to simulate and visualize naval and underwater scenarios in acoustics. It is particularly useful in the field of underwater acoustics for simulating the movement and interactions of various objects like ships and hydrophones in a predefined environment.

Key functionalities of the ScenarioController class include:
- Environment Setup: Define the dimensions of the simulation environment, including width, depth, and height, which are dynamically adjusted based on the positions of the objects in the scenario.
- Object Management: Add and manage various objects within the scenario, such as ships and hydrophones. Each object's position and movement can be simulated and tracked over time.
- Movement Simulation: Simulate the movement of objects within the scenario based on specified parameters such as speed, direction, and time.
- Visualization: Create both 2D and 3D visualizations of the scenario using advanced plotting libraries. The module supports static image generation as well as interactive animations to represent the movement and interaction of objects within the scenario.

The ScenarioController is versatile and can be applied in various aspects of underwater acoustics research, including sonar simulation, acoustic signal processing, and environmental impact studies.

Example of usage:
    scenario = ScenarioController(dimension=3)
    scenario.add_object(ship)
    scenario.add_object(hydrophone)
    scenario.simulate_movement(ship_movements, hydrophone_movements)
    scenario.plot_components(dimension=3)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import os
from labsonar_synthesis.scenario.ship import Ship
from labsonar_synthesis.scenario.hydrophone import Hydrophone


class ScenarioController:
    def __init__(self, dimension=3, max_draft=10):
        """
          Initialize a new ScenarioController instance.

          Args:
              dimension (int, optional): The dimensionality of the scenario (2D or 3D). Defaults to 3.
              max_draft (int, optional): The maximum draft depth for objects type ships in the scenario. Defaults to 10.

          Attributes:
              _dimension (int): Dimensionality of the scenario.
              _width (float): Dynamic width of the scenario based on object positions.
              _depth (float): Dynamic depth of the scenario.
              _height (float): Dynamic height of the scenario, used in 3D scenarios.
              _max_draft (int): Maximum draft depth for objects type ships.
              _objects (list): List to store objects like ships and hydrophones.
        """
        if dimension not in [2, 3]:
            raise ValueError("A dimensão deve ser 2 ou 3.")
        self._dimension = dimension
        self._width = -1
        self._depth = -1
        self._height = -1 if dimension == 3 else None
        self._max_draft = max_draft
        self._objects = []

    def add_object(self, obj):
        """
          Add an object (e.g., ship or hydrophone) to the scenario.

          Args:
              obj (Object): The object to be added to the scenario. Expected to have a 'position' attribute.

          Updates:
              _objects (list): Appends the new object to the scenario's object list.
              _width, _depth, _height (float): Updates the scenario dimensions based on the object's position.
        """
        if not hasattr(obj, 'position') or not isinstance(obj.position, tuple):
            raise ValueError("O objeto deve ter um atributo 'position' do tipo tupla.")
        self._objects.append(obj)
        self._update_dimensions(obj.position)

    def _update_dimensions(self, position):
        if not all(isinstance(coord, (int, float)) for coord in position):
            raise ValueError("As coordenadas da posição devem ser números inteiros ou flutuantes.")
        x, y, z = position
        if self._width < x: self._width = x + 50
        if self._depth < y: self._depth = y + 50
        if self._dimension == 3 and self._height < z: self._height = z + 50


    def simulate_movement(self, ship_movements, hydrophone_movements):
        """
            Simulate the movement of ships and hydrophones within the scenario.

            Args:
                ship_movements (dict): A dictionary mapping ships to their movement instructions.
                hydrophone_movements (dict): A dictionary mapping hydrophones to their movement instructions.

            Processes:
                Iterates through each object in the respective movement dictionaries, updating their positions.
                Detects interactions or noise based on the new positions (not implemented in initial version).
        """
        for obj, movements in ship_movements.items():
            if obj in self._objects:
                obj.move(self, movements)
        for obj, movements in hydrophone_movements.items():
            if obj in self._objects:
                obj.move(self, movements)
    

    def animate_movement(self, ship_movements, hydrophone_movements, filename='movement.gif', fps=20):
        """
            Create an animation of the movement of ships and hydrophones in the scenario.

            Args:
                ship_movements (dict): A dictionary mapping ships to their movement instructions.
                hydrophone_movements (dict): A dictionary mapping hydrophones to their movement instructions.
                filename (str, optional): The filename for saving the animation. Defaults to 'movement.gif'.
                fps (int, optional): Frames per second for the animation. Defaults to 20.

            Returns:
                Saves an animated GIF to the specified filename showing the movement of objects in the scenario.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, self._width)
        ax.set_ylim(0, self._depth)
        ax.set_zlim(0, self._height)
        ax.set_xlabel('Scenario Width (X)')
        ax.set_ylabel('Scenario Length (Y)')
        ax.set_zlabel('Depth (Z)')
        ax.invert_zaxis()

        ships = [ax.plot([], [], [], 'bs')[0] for _ in ship_movements]
        hydrophones = [ax.plot([], [], [], 'r+')[0] for _ in hydrophone_movements]

        def calculate_movements(start_position, end_position, velocity, fps):
          if velocity == 0:  
              return [start_position]  
          distance = np.linalg.norm(np.array(end_position) - np.array(start_position))
          time_in_seconds = distance / velocity
          total_frames = int(time_in_seconds * fps)  # Garantindo que seja inteiro
          dx = (end_position[0] - start_position[0]) / total_frames
          dy = (end_position[1] - start_position[1]) / total_frames
          dz = (end_position[2] - start_position[2]) / total_frames
          return [(start_position[0] + dx * t, start_position[1] + dy * t, start_position[2] + dz * t) for t in range(total_frames)]


        def init():
            for plot in ships + hydrophones:
                plot.set_data([], [])
                plot.set_3d_properties([])
            return ships + hydrophones

        ship_lines = [ax.plot([], [], [], 'g-')[0] for _ in ship_movements]

        def update(frame):
          for ship_plot, ship_line, ship in zip(ships, ship_lines, ship_movements):
              if ship in ship_movements and ship_movements[ship]:
                  end_position, velocity = ship_movements[ship]
                  if frame == 0:
                      start_position = ship.position
                      ship_velocity = velocity
                      ship.movements = calculate_movements(start_position, end_position, ship_velocity, fps)
                  if frame < len(ship.movements):
                      ship.position = ship.movements[frame]
              ship_plot.set_data([ship.position[0]], [ship.position[1]])
              ship_plot.set_3d_properties([ship.position[2]])

              # Desenhar a linha vertical do navio até o fundo
              ship_line.set_data([ship.position[0], ship.position[0]], [ship.position[1], ship.position[1]])
              ship_line.set_3d_properties([self._height, ship.position[2]])  # Altura zero representa o fundo

          for hydrophone_plot, hydrophone in zip(hydrophones, hydrophone_movements):
              if hydrophone in hydrophone_movements and hydrophone_movements[hydrophone]:
                  end_position, velocity = hydrophone_movements[hydrophone]
                  if frame == 0:
                      start_position = hydrophone.position
                      hydrophone_velocity = velocity
                      hydrophone.movements = calculate_movements(start_position, end_position, hydrophone_velocity, fps)
                  if frame < len(hydrophone.movements):
                      hydrophone.position = hydrophone.movements[frame]
              hydrophone_plot.set_data([hydrophone.position[0]], [hydrophone.position[1]])
              hydrophone_plot.set_3d_properties([hydrophone.position[2]])

          return ships + ship_lines +hydrophones

        total_frames = int(15 * fps)  # Duração total da animação em frames (inteiro)
        ani = FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, repeat=False)
        ani.save(filename, writer='pillow', fps=fps)  # Salvando com o Pillow
        plt.close(fig)



    def plot_components(self, dimension=2, save_path='plots'):
        """
            Plot the current positions of the objects in the scenario.

            Args:
                dimension (int, optional): Whether to plot in 2D or 3D. Defaults to 2.
                save_path (str, optional): The path to save the plot image. Defaults to 'plots'.

            Returns:
                Generates and saves a plot of the current scenario in the specified dimensionality.
                The plot is saved as an image in the specified save path.
        """
        if dimension not in [2, 3]:
            raise ValueError("A dimensão deve ser 2 ou 3.")
        if dimension == 3:
            if not os.path.exists(save_path):
              os.makedirs(save_path)

            fig = go.Figure()

            for obj in self._objects:
                if isinstance(obj, Ship):
                    fig.add_trace(go.Scatter3d(
                        x=[obj.position[0]],
                        y=[obj.position[1]],
                        z=[obj.position[2]],
                        mode='markers+text',
                        marker=dict(size=5, color='blue'),
                        name='Navio',
                        text=[f'Navio ({obj.position[0]}, {obj.position[1]}, {obj.position[2]})'],
                        textposition='bottom center'
                    ))

                elif isinstance(obj, Hydrophone):
                    fig.add_trace(go.Scatter3d(
                        x=[obj.position[0]],
                        y=[obj.position[1]],
                        z=[obj.position[2]],
                        mode='markers+text',
                        marker=dict(size=5, color='red'),
                        name='Hidrofone',
                        text=[f'Hidrofone ({obj.position[0]}, {obj.position[1]}, {obj.position[2]})'],
                        textposition='bottom center'
                    ))

            fig.update_layout(
                scene=dict(
                    xaxis_title='Scenario Width (X)',
                    yaxis_title='Scenario Length (Y)',
                    zaxis_title='Depth (Z)',
                    xaxis=dict(range=[0, self._width]),
                    yaxis=dict(range=[0, self._depth]),
                    zaxis=dict(range=[0, self._height], autorange='reversed'),
                ),
                title='Component Positions in Scenario'
            )
            filename = f'scenario_plot_{dimension}D.png'
            fig.write_image(os.path.join(save_path, filename))

        
