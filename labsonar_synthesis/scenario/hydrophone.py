class Hydrophone:
    def __init__(self, position):
        self._position = position
        self.movements = []

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value


    def calculate_movements(self, end_position, time_in_seconds, fps):
        total_frames = time_in_seconds * fps
        dx = (end_position[0] - self._position[0]) / total_frames
        dy = (end_position[1] - self._position[1]) / total_frames
        dz = (end_position[2] - self._position[2]) / total_frames
        self.movements = [(self._position[0] + dx * t, self._position[1] + dy * t, self._position[2] + dz * t) for t in range(total_frames + 1)]

    def update_position(self, displacement):
        self._position = displacement


    def calculate_distance(self, source_position):
        return sum((sp - hp) ** 2 for sp, hp in zip(source_position, self.position)) ** 0.5
