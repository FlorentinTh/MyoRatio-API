import math
import os
from typing import Optional

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from myoratio.api.helpers import PathHelper, PlotHelper
from myoratio.data import Column, Frequencies, _Data
from myoratio.data.processing.resample import Resample
from myoratio.task import Analysis


class IMU(_Data):
    def __init__(self, base_path: str, csv_file: str, analysis: str) -> None:
        self._csv_file = csv_file
        self._base_path = base_path
        self._csv_path = self.get_csv_path()

        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from ResponseStatus, but got {analysis}")

        _Data.__init__(self, csv_file, is_imu=True)

    def _get_accelerometer_raw_data(self) -> pd.DataFrame:
        if (
            self._analysis == Analysis.EXTENSION.value
            or self._analysis == Analysis.FLEXION.value
        ):
            data_acc_raw = self._get_column_data(
                Column.ACCELEROMETER_TIBIALIS_ANTERIOR.value
            )
        else:
            data_acc_raw = self._get_column_data(
                Column.ACCELEROMETER_TENSOR_FASCIAE_LATAE.value
            )

        nb_imu_rows_to_keep = math.ceil(
            self._get_total_recording_time() * Frequencies.IMU.value
        )
        return data_acc_raw.iloc[:nb_imu_rows_to_keep]

    def _compute_angle(self, resampled_data: np.ndarray) -> pd.DataFrame:
        accelerometer_x = resampled_data[:, 0]
        accelerometer_y = resampled_data[:, 1]
        accelerometer_z = resampled_data[:, 2]

        angle_z = []

        for i, column in enumerate(resampled_data):
            if self._analysis == Analysis.EXTENSION.value:
                pitch = math.sqrt(accelerometer_x[i] ** 2 + accelerometer_z[i] ** 2)

                if pitch != 0.0:
                    angle_z.extend(
                        [180 * (math.atan(-accelerometer_y[i] / pitch) / math.pi)]
                    )
            else:
                if abs(accelerometer_y[i]) != 0.0:
                    angle_z.extend(
                        [
                            90
                            - (
                                180
                                * (
                                    math.atan(
                                        accelerometer_x[i] / abs(accelerometer_y[i])
                                    )
                                    / math.pi
                                )
                            )
                        ]
                    )

        emg_trig_data = self._get_column_data(Column.EMG_TRIG.value)

        time_emg_trig = self._dataframe.iloc[
            :, self._dataframe.columns.get_loc(emg_trig_data.columns[0]) - 1
        ]

        data = pd.concat(
            [time_emg_trig, pd.DataFrame(angle_z, columns=["y"])], axis=1
        ).dropna()

        data.set_index(data.columns[0], inplace=True)

        return data

    def _reduce_angle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.reset_index(drop=False)
        data_length = len(str(len(data)))

        i = 0
        step = "1"
        while i < (data_length - 3):
            i = i + 1
            step += "0"

        return data.iloc[:: int(step), :]

    def _write_angles(
        self, data: pd.DataFrame, file_type: str, prefix: Optional[str] = None
    ) -> None:
        if file_type == "JSON":
            ext = ".json"
            data.rename(columns={f"{data.columns[0]}": "x"}, inplace=True)
        elif file_type == "CSV":
            ext = ".csv"
        else:
            raise ValueError("file_type argument must be JSON or CSV")

        if prefix is None:
            output_filename = f"angle_{os.path.splitext(self._csv_path[1])[0]}{ext}"
        else:
            output_filename = (
                f"{prefix}_angle_{os.path.splitext(self._csv_path[1])[0]}{ext}"
            )

        participant_metadata_folder = PathHelper.get_participant_metadata_folder(
            self._base_path, self._csv_path
        )

        file_output_path = os.path.join(participant_metadata_folder, output_filename)

        if file_type == "JSON":
            data.to_json(file_output_path, orient="records")
        elif file_type == "CSV":
            data.to_csv(file_output_path, sep="\t", encoding="utf-8")

    def start_processing(self) -> None:
        indexes = np.where(self._dataframe.iloc[:, 0].isna())[0]

        if len(indexes) > 0:
            self._dataframe = self._dataframe.iloc[: indexes[0], :]

        data_acc = self._get_accelerometer_raw_data()

        resampled_acc_data = Resample(
            data_acc, Frequencies.EMG_TRIG.value, Frequencies.IMU.value
        ).get_data()

        angle_data = self._compute_angle(resampled_acc_data)

        reduced_angle_data = self._reduce_angle_data(angle_data)

        self._write_angles(reduced_angle_data, "JSON", prefix="small")

        filtered_angle_data = savgol_filter(reduced_angle_data["y"], 10, 1)
        filtered_angle_data = pd.DataFrame(
            {
                reduced_angle_data.columns[0]: reduced_angle_data[
                    reduced_angle_data.columns[0]
                ],
                "y": filtered_angle_data,
            }
        )

        self._write_angles(filtered_angle_data, "JSON", prefix="filtered")

        plot_helper = PlotHelper(self._csv_path, angle_data)
        plot_helper.build_plot(
            legend="z-axis angle", x_label="Seconds", y_label="Degrees"
        )
        plot_helper.save_plot(self._base_path, prefix="plot_angle")

        self._write_angles(angle_data, "CSV", prefix="full")
