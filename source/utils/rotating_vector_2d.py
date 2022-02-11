from utils.math_ import tau, to_cartesian


class RotatingVector2D:
    def __init__(self, frequency, magnitude, direction):
        self._frequency = frequency
        self._magnitude = magnitude
        self._direction = direction
        self.compute_vector()

    @property
    def frequency(self):
        return self._frequency

    @property
    def magnitude(self):
        return self._magnitude
    
    @property
    def direction(self):
        return self._direction

    @property
    def vector(self):
        return self._vector

    def compute_vector(self):
        self._vector = to_cartesian(self._magnitude, self._direction)

    def update(self, time_elapsed):
        self._direction += time_elapsed * self._frequency * tau
        self._direction %= tau

        self.compute_vector()
