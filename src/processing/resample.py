from fractions import Fraction

import numpy as np
import pandas as pd
from scipy import signal


class Resample:
    def __init__(self, data: pd.DataFrame, high_frequency: float = None,
                 low_frequency: float = None, fixed_value: int = None):
        self._data = data
        self._high_frequency = high_frequency
        self._low_frequency = low_frequency
        self._fixed_value = fixed_value

    def get_data(self) -> np.array:
        if self._fixed_value is None:
            frequency_fraction = Fraction(self._high_frequency / self._low_frequency).limit_denominator(1000)
            return signal.resample_poly(self._data, frequency_fraction.numerator, frequency_fraction.denominator)
        else:
            return signal.resample_poly(self._data, self._fixed_value, len(self._data))
