"""Naval and Underwater Scenario Simulation Program

This program utilizes the ScenarioController module to simulate and visualize naval and underwater scenarios.
It includes the addition and movement simulation of various objects like ships and hydrophones in a predefined environment.

"""
import random
from labsonar_synthesis.scenario.scenario_controller import ScenarioController
from labsonar_synthesis.scenario.ship import Ship
from labsonar_synthesis.scenario.hydrophone import Hydrophone


def create_random_position(dimension):
    """Generate a random position in the scenario."""
    return tuple(random.uniform(0, 100) for _ in range(dimension))


def main():
    """Main function for the naval and underwater scenario simulation program."""

    # Initialize the ScenarioController
    dimension = 3
    scenario = ScenarioController(dimension=dimension)

    # Create and add ships and hydrophones to the scenario
    for _ in range(5):
        ship_position = create_random_position(dimension)
        hydrophone_position = create_random_position(dimension)
        ship = Ship(ship_position)
        hydrophone = Hydrophone(hydrophone_position)
        scenario.add_object(ship)
        scenario.add_object(hydrophone)

    # Define movements for ships and hydrophones
    ship_movements = {
        ship: (create_random_position(dimension), random.uniform(0, 10)) for ship in scenario.ships
    }
    hydrophone_movements = {
        hydrophone: (create_random_position(dimension), random.uniform(0, 5)) for hydrophone in scenario.hydrophones
    }

    # Simulate movements
    scenario.simulate_movement(ship_movements, hydrophone_movements)

    # Visualize the scenario
    scenario.plot_components(dimension=dimension)
    scenario.animate_movement(ship_movements, hydrophone_movements, filename='scenario_animation.gif')

    print("Scenario simulation and visualization completed.")


if __name__ == "__main__":
    main()
