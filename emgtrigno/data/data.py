import os
from enum import Enum
from typing import Optional

import dask.dataframe.io.csv as dd
import pandas as pd


class Column(Enum):
    EMG_TRIG = 0
    EMG_IM = 1
    ACCELEROMETER_TIBIALIS_ANTERIOR = 2
    ACCELEROMETER_TENSOR_FASCIAE_LATAE = 3


class _Data:
    def __init__(self, csv_file: str, is_imu: bool = False):
        self._csv_file = csv_file

        try:
            if is_imu is True:
                self._dataframe = dd.read_csv(self._csv_file).compute()
            else:
                self._dataframe = pd.read_csv(
                    self._csv_file, engine="c", encoding="utf-8"
                )
        except pd.errors.ParserError as error:
            raise pd.errors.ParserError(error)

    def _get_column_data(self, column: int) -> pd.DataFrame:
        if column not in [column.value for column in Column]:
            raise ValueError(f"Expected a value from ResponseStatus, but got {column}")

        if column == 0:
            return self._dataframe.filter(regex=r"^(?=.*EMG)(?!.*\(IM\)).*")
        elif column == 1:
            return self._dataframe.filter(regex=r"^(?=.*EMG)(?=.*\(IM\)).*")
        elif column == 2:
            return self._dataframe.filter(regex=r"^(?=.*TIBIALIS ANTERIOR)(?=.*ACC).*")
        else:
            return self._dataframe.filter(regex=r"^(?=.*TENSOR FASCIAE LATAE)(?=.*ACC).*")

    def _get_time_emg(self, data: pd.DataFrame, skip: Optional[int] = None) -> pd.Series:
        if skip is None:
            return self._dataframe.iloc[
                :, self._dataframe.columns.get_loc(data.columns[0]) - 1
            ]
        else:
            return self._dataframe.iloc[
                :skip, self._dataframe.columns.get_loc(data.columns[0]) - 1
            ]

    def _get_total_recording_time(self) -> float:
        emg_trig_data = self._get_column_data(Column.EMG_TRIG.value)
        emg_trig_time = self._get_time_emg(emg_trig_data)
        return emg_trig_time.dropna().iloc[-1:].tolist()[0]

    def get_csv_path(self) -> tuple:
        return os.path.split(self._csv_file)
