import math

import numpy
from attr import attrs, attrib
from pandas import get_dummies

from ._base import BaseSeriesPreprocessor


@attrs
class CategoricalSeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'categorical'
    dtype = object

    fillna = attrib(default=None)
    default = attrib(default=float('nan'))

    def process(self, series):
        series = series.map(self.get_category, na_action='ignore')

        if self.fillna is not None:
            series = series.fillna(self.fillna)

        if not (isinstance(self.default, float) and math.isnan(self.default)):
            series = self._default_to_nan(series)

        dummies = get_dummies(series).astype(numpy.uint8)
        return dummies.rename(columns=self.get_column)

    def _default_to_nan(self, series):
        default = self.default

        def replacer(x):
            if isinstance(x, float) and numpy.isnan(x):
                return 'NAN'
            elif default in (None, True, False) and x is default:
                return float('nan')
            elif x == default:
                return float('nan')
            else:
                return x

        return series.map(replacer)

    @staticmethod
    def get_category(value):
        return value

    @staticmethod
    def get_column(category):
        return str(category)
