from collections import deque
from dataclasses import dataclass
from typing import Callable

import scipy
from scipy.integrate import quad

from utils.math_ import array, tau, to_complex_number, to_polar
from utils.rotating_vector_2d import RotatingVector2D


@dataclass
class ComplexFourierSeriesAnimation:
    _function: Callable[[float], float]
    _num_terms: int
    _path_maxlen: int

    def __post_init__(self):
        self.init_vectors()
        self._path = deque(maxlen=self._path_maxlen)

    @property
    def function(self):
        return self._function

    @property
    def num_terms(self):
        return self._num_terms

    @property
    def path_maxlen(self):
        return self._path_maxlen

    @property
    def vectors(self):
        return self._vectors

    @property
    def path(self):
        return self._path

    def init_vectors(self):
        self._vectors = [None for _ in range(self._num_terms)]

        interval = (0, 1)
        minimum_frequency = -self._num_terms // 2

        for i in range(self._num_terms):
            frequency = minimum_frequency + i

            def augmented_function(t):
                return self._function(t) * to_complex_number(1, -t * frequency * tau)

            # numerically integrate the augmented function to determine the vector
            real = quad(lambda t: scipy.real(augmented_function(t)), *interval)[0]
            imag = quad(lambda t: scipy.imag(augmented_function(t)), *interval)[0]

            magnitude, direction = to_polar(real + (imag * 1j))
            
            self._vectors[i] = RotatingVector2D(frequency, magnitude, direction)
        
        self._vectors.sort(key=lambda vector: vector.magnitude, reverse=True)

    def update(self, time_elapsed):
        end_point = array((0, 0))

        for vector in self._vectors:
            vector.update(time_elapsed)
            end_point += vector.vector
        
        self._path.append(end_point)
