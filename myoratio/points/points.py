import random

import pandas as pd

from myoratio.stage import Stage


class Points:
    def __init__(self, stage: str, json_file_path: str) -> None:
        if stage in [stage.value for stage in Stage]:
            self._stage = stage
        else:
            raise ValueError(f"Expected a value from ResponseStatus, but got {stage}")

        self._dataframe = None

        try:
            self._dataframe = pd.read_json(
                json_file_path, precise_float=False, encoding="utf-8", convert_dates=False
            )

            self._dataframe["x"] = self._dataframe["x"].astype("float32")

        except pd.errors.ParserError as error:
            raise (error)

    def _dumb_points_retrieval(self) -> list[dict[str, float]]:
        if self._dataframe is not None:
            dataframe_length = len(self._dataframe)
        else:
            raise ValueError("class Points was not properly initialized")

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

        points = [
            {
                "x": self._dataframe.at[point_1x_index, "x"].astype(str),
                "y": self._dataframe.at[point_1x_index, "y"],
            },
            {
                "x": self._dataframe.at[point_2x_index, "x"].astype(str),
                "y": self._dataframe.at[point_2x_index, "y"],
            },
        ]

        return points

    def _points_retrieval(self) -> list[dict[str, float]]:
        if self._dataframe is None:
            raise ValueError("class Points was not properly initialized")

        window_size = 10
        rolling_values = self._dataframe["y"].rolling(window_size, min_periods=1).mean()

        start_index = None
        stop_index = None

        if self._stage == Stage.CONCENTRIC.value:
            forward_limit = 1

            for i in range(len(rolling_values)):
                current = int(rolling_values[i])

                if forward_limit < i < len(rolling_values) - forward_limit:
                    if start_index is None:
                        if current < int(rolling_values[i - 1]):
                            start_index = i - 1

                    if stop_index is None and start_index is not None:
                        if int(rolling_values[i + 1]) > current:
                            for j in range(i - 1, -1, -1):
                                if int(rolling_values[j - 2]) > int(
                                    rolling_values[j - 1]
                                ):
                                    stop_index = j - 1
                                    break
        elif self._stage == Stage.ECCENTRIC.value:
            forward_limit = 2

            for i in range(len(rolling_values) - 1, -1, -1):
                current = int(rolling_values[i])

                if len(rolling_values) - forward_limit > i > forward_limit:
                    if start_index is None:
                        if (
                            current
                            < int(rolling_values[i + 1])
                            < int(rolling_values[i + 2])
                        ):
                            start_index = i

                    if stop_index is None and start_index is not None:
                        if int(rolling_values[i - 1]) > current:
                            for j in range(i, len(rolling_values) - 1, 1):
                                if int(rolling_values[j]) < int(rolling_values[j + 1]):
                                    stop_index = j
                                    break

        if start_index is None or stop_index is None:
            raise ValueError("Automatic points identification failed")
        else:
            if stop_index > start_index:
                point_1x_index = start_index
                point_2x_index = stop_index
            else:
                point_1x_index = stop_index
                point_2x_index = start_index

        return [
            {
                "x": self._dataframe.at[point_1x_index, "x"].astype(str),
                "y": self._dataframe.at[point_1x_index, "y"],
            },
            {
                "x": self._dataframe.at[point_2x_index, "x"].astype(str),
                "y": self._dataframe.at[point_2x_index, "y"],
            },
        ]

    def get_points(self) -> list[dict[str, float]]:
        return self._points_retrieval()
