from fractions import Fraction
from scipy import signal


class Resample:
    def __init__(self, data, high_frequency=None, low_frequency=None, fixed_value=None):
        self._data = data
        self._high_frequency = high_frequency
        self._low_frequency = low_frequency
        self._fixed_value = fixed_value

    def get_data(self):
        if self._fixed_value is None:
            frequency_fraction = Fraction(self._high_frequency / self._low_frequency).limit_denominator(1000)
            return signal.resample_poly(self._data, frequency_fraction.numerator, frequency_fraction.denominator)
        else :
            return signal.resample_poly(self._data, self._fixed_value, len(self._data))
