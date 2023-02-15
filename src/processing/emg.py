import math
from enum import Enum
from typing import Optional

import numpy as np
import pandas as pd
from scipy import integrate, signal

from src.helpers import CSVHelper

from .data import Column, _Data
from .frequencies import Frequency
from .resample import Resample


class FilterOptions(Enum):
    ORDER = 4
    LOWPASS_FREQUENCY_CUTOFF = 20
    HIGHPASS_FREQUENCY_CUTOFF = 450


class NormalizationOptions(Enum):
    LENGTH = 1000


class EMG(_Data):
    def __init__(self, base_path: str, csv_file: str, stage: str):
        self._csv_file = csv_file
        self._base_path = base_path
        self._csv_path = self.get_csv_path()
        self._stage = stage
        _Data.__init__(self, csv_file)

        self._emg_trig_data = None
        self._emg_trig_time = None
        self._emg_im_data = None

    def _get_emg_trig_raw_data(self) -> None:
        self._emg_trig_data = self._get_column_data(Column.EMG_TRIG.value)
        self._emg_trig_time = self._get_time_emg(self._emg_trig_data)
        self._emg_trig_data = pd.concat(
            [self._emg_trig_time, self._emg_trig_data], axis=1
        )
        self._emg_trig_data.set_index(self._emg_trig_data.columns[0], inplace=True)

    def _get_emg_im_raw_data(self) -> None:
        self._emg_im_data = self._get_column_data(Column.EMG_IM.value)
        nb_emg_im_rows_to_keep = math.ceil(
            self._get_total_recording_time() * Frequency.EMG_IM.value
        )
        self._emg_im_data = self._emg_im_data.iloc[:nb_emg_im_rows_to_keep]
        emg_im_time = self._get_time_emg(self._emg_im_data, skip=nb_emg_im_rows_to_keep)
        self._emg_im_data = pd.concat([emg_im_time, self._emg_im_data], axis=1)
        self._emg_im_data.set_index(self._emg_im_data.columns[0], inplace=True)

    def _remove_mean_all_emg_data(
        self, resampled_emg_im_data: pd.DataFrame
    ) -> pd.DataFrame:

        if self._emg_trig_data is not None:
            data_all_emg = pd.concat([self._emg_trig_data, resampled_emg_im_data], axis=1)
            data_mean_all_emg_removed = pd.DataFrame(np.zeros(data_all_emg.shape))
            data_mean_all_emg_removed.index = data_all_emg.index
            data_mean_all_emg_removed.columns = data_all_emg.columns

            for i, column in enumerate(data_all_emg):
                mean = data_all_emg[column].mean()
                computed_column = data_all_emg[column].apply(lambda value: (value - mean))
                data_mean_all_emg_removed[
                    data_mean_all_emg_removed[column].name
                ] = computed_column

            return data_mean_all_emg_removed
        else:
            raise ValueError(f"class EMG object was not properly initialized")

    def _filter_all_emg_data(
        self, removed_mean_all_emg_data: pd.DataFrame
    ) -> pd.DataFrame:
        order = FilterOptions.ORDER.value
        lowpass_frequency_cutoff = FilterOptions.LOWPASS_FREQUENCY_CUTOFF.value
        highpass_frequency_cutoff = FilterOptions.HIGHPASS_FREQUENCY_CUTOFF.value
        iir_filter_sos = signal.butter(
            order,
            [lowpass_frequency_cutoff, highpass_frequency_cutoff],
            btype="bandpass",
            fs=Frequency.EMG_TRIG.value,
            output="sos",
        )
        all_emg_filtered_data = pd.DataFrame()

        for i, column in enumerate(removed_mean_all_emg_data):
            filtered = signal.sosfilt(
                iir_filter_sos, removed_mean_all_emg_data[column].to_numpy()
            )
            all_emg_filtered_data[removed_mean_all_emg_data[column].name] = pd.Series(
                filtered
            )

        if self._emg_trig_time is not None:
            all_emg_filtered_data = pd.concat(
                [self._emg_trig_time, all_emg_filtered_data], axis=1
            )
        else:
            raise ValueError(f"class EMG object was not properly initialized")

        all_emg_filtered_data.set_index(all_emg_filtered_data.columns[0], inplace=True)
        return all_emg_filtered_data

    def _extract_rms_envelope_from_all_emg_data(
        self, all_emg_filtered_data: pd.DataFrame, window_size: float
    ) -> pd.DataFrame:
        window = signal.windows.boxcar(round(Frequency.EMG_TRIG.value * window_size))
        n_pad = len(window) - 1
        all_emg_rms_envelope_data = pd.DataFrame()

        for i, column in enumerate(all_emg_filtered_data):
            all_emg_power_data = np.square(all_emg_filtered_data[column].to_numpy())
            all_emg_power_padded_data = np.pad(
                all_emg_power_data, (n_pad // 2, n_pad - n_pad // 2), mode="constant"
            )
            all_emg_power_convolution_data = np.convolve(
                all_emg_power_padded_data, window, mode="valid"
            )
            final_computed_column = np.sqrt(
                np.divide(all_emg_power_convolution_data, np.sum(window))
            )
            all_emg_rms_envelope_data[all_emg_filtered_data[column].name] = pd.Series(
                final_computed_column
            )

        if self._emg_trig_time is not None:
            all_emg_rms_envelope_data = pd.concat(
                [self._emg_trig_time, all_emg_rms_envelope_data], axis=1
            ).dropna()
        else:
            raise ValueError(f"class EMG object was not properly initialized")

        return all_emg_rms_envelope_data

    @staticmethod
    def _get_point_index(data: pd.DataFrame, point_x: float, point_y: float) -> dict:
        return {
            "x": data.index[data["X[s]"] == point_x].tolist()[0],
            "y": data.index[data["X[s]"] == point_y].tolist()[0],
        }

    def start_processing(
        self, window_size: float, point_1x: float, point_2x: float
    ) -> None:
        self._get_emg_trig_raw_data()
        self._get_emg_im_raw_data()

        if self._emg_im_data is not None:
            resampled_emg_im_data = Resample(
                self._emg_im_data, Frequency.EMG_TRIG.value, Frequency.EMG_IM.value
            ).get_data()
        else:
            raise ValueError(f"class EMG object was not properly initialized")

        resampled_emg_im_data = pd.DataFrame(
            resampled_emg_im_data, columns=self._emg_im_data.columns
        )

        if self._emg_trig_time is not None:
            resampled_emg_im_data = pd.concat(
                [self._emg_trig_time, resampled_emg_im_data], axis=1
            ).dropna()
        else:
            raise ValueError(f"class EMG object was not properly initialized")

        resampled_emg_im_data.set_index(resampled_emg_im_data.columns[0], inplace=True)

        removed_mean_all_emg_data = self._remove_mean_all_emg_data(resampled_emg_im_data)

        all_emg_filtered_data = self._filter_all_emg_data(removed_mean_all_emg_data)

        all_emg_rms_envelope_data = self._extract_rms_envelope_from_all_emg_data(
            all_emg_filtered_data, window_size
        )

        points = self._get_point_index(all_emg_rms_envelope_data, point_1x, point_2x)

        all_emg_between_points_data = all_emg_rms_envelope_data.iloc[
            points["x"] : points["y"], :
        ]

        normalized_envelope_all_emg_data = Resample(
            all_emg_between_points_data,
            fixed_value=NormalizationOptions.LENGTH.value,
        ).get_data()

        normalized_envelope_all_emg_data = pd.DataFrame(
            normalized_envelope_all_emg_data,
            columns=all_emg_between_points_data.columns,
        )

        normalized_envelope_all_emg_data.set_index(
            normalized_envelope_all_emg_data.columns[0], inplace=True
        )

        CSVHelper.write_normalized_envelope(
            self._base_path,
            self._csv_path,
            self._stage,
            normalized_envelope_all_emg_data,
        )
