import math

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from emgtrigno.api.helpers import JSONHelper, PlotHelper
from emgtrigno.data import Column, Frequencies, _Data
from emgtrigno.data.processing.resample import Resample
from emgtrigno.task import Analysis


class IMU(_Data):
    def __init__(self, base_path: str, csv_file: str, analysis: str):
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
        accelerometer_x1 = resampled_data[:, 0]
        accelerometer_y1 = resampled_data[:, 1]
        accelerometer_z1 = resampled_data[:, 2]

        # accelerometer_x = []
        # accelerometer_y = []
        accelerometer_z = []

        for i, column in enumerate(resampled_data):
            total = math.sqrt(
                accelerometer_x1[i] ** 2
                + accelerometer_y1[i] ** 2
                + accelerometer_z1[i] ** 2
            )

            if total == 0.0:
                # accelerometer_x.append(math.asin(0) * 180 / math.pi)
                # accelerometer_y.append(math.asin(0) * 180 / math.pi)
                accelerometer_z.append(math.acos(0) * 180 / math.pi)
            else:
                # accelerometer_x.append(math.asin(accelerometer_x1[i] / total) * 180 / math.pi)
                # accelerometer_y.append(math.asin(accelerometer_y1[i] / total) * 180 / math.pi)
                accelerometer_z.append(
                    math.acos(accelerometer_z1[i] / total) * 180 / math.pi
                )

        emg_trig_data = self._get_column_data(Column.EMG_TRIG.value)
        time_emg_trig = self._dataframe.iloc[
            :, self._dataframe.columns.get_loc(emg_trig_data.columns[0]) - 1
        ]
        data = pd.concat(
            [time_emg_trig, pd.DataFrame(accelerometer_z, columns=["y"])], axis=1
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
        JSONHelper.write_angle_file(
            self._base_path, self._csv_path, reduced_angle_data, prefix="small"
        )

        filtered_angle_data = savgol_filter(reduced_angle_data["y"], 10, 1)
        filtered_angle_data = pd.DataFrame(
            {
                reduced_angle_data.columns[0]: reduced_angle_data[
                    reduced_angle_data.columns[0]
                ],
                "y": filtered_angle_data,
            }
        )

        JSONHelper.write_angle_file(
            self._base_path, self._csv_path, filtered_angle_data, prefix="filtered"
        )

        plot_helper = PlotHelper(self._csv_path, angle_data)
        plot_helper.build_plot(
            legend="z-axis angle", x_label="Seconds", y_label="Degrees"
        )
        plot_helper.save_plot(self._base_path, prefix="plot_angle")
        angle_data.reset_index(inplace=True)
        JSONHelper.write_angle_file(self._base_path, self._csv_path, angle_data, prefix='full')
