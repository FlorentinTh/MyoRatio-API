import random
from enum import Enum

import pandas as pd


class Stage(Enum):
    CONCENTRIC = "concentric"
    ECCENTRIC = "eccentric"


class Points:
    def __init__(self, stage: str, json_file_path: str) -> None:
        self._stage = stage
        self._dataframe = None

        try:
            self._dataframe = pd.read_json(json_file_path)
        except pd.errors.ParserError as error:
            raise (error)

    def _dumb_points_retrieval(self) -> list[dict[str, float]]:
        if self._dataframe is not None:
            dataframe_length = len(self._dataframe)
        else:
            raise ValueError(f"class Points was not properly initialized")

        if self._stage == Stage.CONCENTRIC.value:
            point_1x_index = random.randint(
                round(dataframe_length / 8 - (((dataframe_length / 8) * 5) / 100)),
                round(dataframe_length / 8),
            )

            point_2x_index = random.randint(
                round(dataframe_length / 3 + (((dataframe_length / 3) * 5) / 100)),
                round(dataframe_length / 3 + (((dataframe_length / 3) * 10) / 100)),
            )
        else:
            point_1x_index = random.randint(
                round(dataframe_length / 2 - (((dataframe_length / 2) * 10) / 100)),
                round(dataframe_length / 2 - (((dataframe_length / 2) * 5) / 100)),
            )

            point_2x_index = random.randint(
                round(3 * (dataframe_length / 4)),
                round(
                    (
                        (3 * (dataframe_length / 4))
                        + (((3 * (dataframe_length / 4)) * 5) / 100)
                    )
                ),
            )

        return [
            {
                "x": self._dataframe._get_value(point_1x_index, "x"),
                "y": self._dataframe._get_value(point_1x_index, "y"),
            },
            {
                "x": self._dataframe._get_value(point_2x_index, "x"),
                "y": self._dataframe._get_value(point_2x_index, "y"),
            },
        ]

    def _points_retrieval(self) -> list[dict[str, float]]:
        # for window in df.rolling(window=20):
        #     print(window.mean(), window.min(), window.max())
        #     print("------------")
        return []

    def get_points(self) -> list[dict[str, float]]:
        return self._dumb_points_retrieval()
