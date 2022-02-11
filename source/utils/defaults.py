from functools import partial, reduce

import numpy as np


# define a decorator for setting attributes of a function
def set_attributes(**attributes):
    def get_function(function):
        for name, value in attributes.items():
            setattr(function, name, value)
        return function
    return get_function

# define a function for using numpy with extra-precision dtype where applicable
@set_attributes(default_kwargs=dict(dtype=np.longdouble))
def numpy_(*attribute_names):
    return partial(
        reduce(getattr, attribute_names, np),
        **numpy_.default_kwargs
    )
