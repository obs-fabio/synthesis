class Ship:
    def __init__(self, position):
        """
            Initialize a Ship object with a starting position.

            Args:
                position (tuple): A tuple of 2 (for 2D) or 3 (for 3D) coordinates representing the initial position of the ship.

            Raises:
                ValueError: If the position tuple does not have 2 or 3 elements.
        """
        if len(position) == 2:  
            self._position = position + (0,)  
        elif len(position) == 3:  
            self._position = position
        else:
            raise ValueError("A posição deve ser uma tupla de 2 ou 3 coordenadas.")
        self.movements = []

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def calculate_movements(self, end_position, time_in_seconds, fps):
        """
            Calculate the incremental movements of the ship towards a target position over a given time.

            Args:
                end_position (tuple): The target position for the ship to move towards.
                time_in_seconds (int): Total time in seconds for the ship to reach the end position.
                fps (int): Frames per second, used to determine the total number of increments.
         """
        total_frames = time_in_seconds * fps
        dx = (end_position[0] - self._position[0]) / total_frames
        dy = (end_position[1] - self._position[1]) / total_frames
        dz = (end_position[2] - self._position[2]) / total_frames
        self.movements = [(self._position[0] + dx * t, self._position[1] + dy * t, self._position[2] + dz * t) for t in range(total_frames + 1)]

    def update_position(self, displacement):
        """
            Update the ship's position based on the given displacement.

            Args:
                displacement (tuple): A tuple of 2 or 3 coordinates representing the new position of the ship.
        """
        self._position = displacement


    def calculate_distance(self, source_position):
        return sum((sp - hp) ** 2 for sp, hp in zip(source_position, self.position)) ** 0.5



class NoiseProfile:
    """
        Initialize a NoiseProfile object with a specific noise type and level.

        Args:
            noise_type (str): The type of noise (e.g., 'motor', 'sonar').
            level (int or float): The level of noise.
    """
    def __init__(self, noise_type, level):
        self._noise_type = noise_type 
        self._level = level  

    @property
    def noise_type(self):
        return self._noise_type

    @noise_type.setter
    def noise_type(self, value):
        self._noise_type = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

class OceanCurrent:
    """
        Initialize an OceanCurrent object with a specific direction and strength.

        Args:
            direction (tuple): A tuple representing the direction of the current.
            strength (int or float): The strength of the current.
    """
    def __init__(self, direction, strength):
        self._direction = direction  
        self._strength = strength  

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = value

    def calculate_effect(self, position):
        """
        Calculate the effect of the current on a given position.

        Args:
            position (tuple): The position of an object to calculate the current's effect on.

        Returns:
            tuple: The modified position after accounting for the current's effect.
        """
        return tuple(d * self._strength for d in self._direction)
