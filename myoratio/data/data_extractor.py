import pandas as pd


class DataExtractor:
    def __init__(self, data: pd.DataFrame, point_x: float, point_y: float) -> None:
        self._data = data
        self._point_x = point_x
        self._point_y = point_y

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        self._data = data

    def _get_point_index(self) -> dict:
        return {
            "x": self._data.index[self._data["X[s]"] == self._point_x].tolist()[0],
            "y": self._data.index[self._data["X[s]"] == self._point_y].tolist()[0],
        }

    def extract_data(self) -> pd.DataFrame:
        points = self._get_point_index()
        all_data_between_points = self._data.iloc[points["x"] : points["y"], :]
        return all_data_between_points.drop(all_data_between_points.columns[0], axis=1)
