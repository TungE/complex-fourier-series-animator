from collections import deque

import scipy
from scipy.integrate import quad

from utils.math_ import array, tau, to_complex_number, to_polar
from utils.rotating_vector_2d import RotatingVector2D


class ComplexFourierSeriesAnimation:
    def __init__(self, function, num_terms, path_maxlen):
        self._function = function
        self._num_terms = num_terms
        self._path = deque(maxlen=path_maxlen)
        self.init_vectors()

    @property
    def function(self):
        return self._function

    @property
    def num_terms(self):
        return self._num_terms

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
