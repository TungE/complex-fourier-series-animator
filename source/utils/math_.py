import numpy as np

from utils.defaults import numpy_ as np_


tau = 2 * np.pi


def sin(angle):
    return np_('sin')(angle)

def cos(angle):
    return np_('cos')(angle)

def array(*args, **kwargs):
    return np_('array')(*args, **kwargs)

def get_distance(point0, point1):
    return np.linalg.norm(array(point0) - array(point1))

def to_polar(complex_number):
    magnitude = np.abs(complex_number)
    direction = np.angle(complex_number)
    return magnitude, direction

def to_complex_number(magnitude, direction):
    complex_number = magnitude * np.exp(direction * 1j)
    return complex_number

def to_cartesian(magnitude, direction):
    complex_number = to_complex_number(magnitude, direction)
    return array((complex_number.real, complex_number.imag))
