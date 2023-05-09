import json
import os
from typing import Optional

import pandas as pd
from scipy import integrate


class Areas:
    def __init__(
        self, data_path: str, stage: str, csv_files: Optional[list[str]] = None
    ) -> None:
        self._data_path = data_path
        self._stage = stage

        if csv_files is not None:
            self._dataframes = []

            for csv_file in csv_files:
                try:
                    dataframe = pd.read_csv(
                        csv_file, sep="\t", encoding="utf-8", engine="c"
                    )
                    dataframe.set_index(dataframe.columns[0], inplace=True)
                    self._dataframes.append(dataframe)
                except pd.errors.ParserError as error:
                    raise pd.errors.ParserError(error)

    def _compute_areas(self, data: pd.DataFrame) -> pd.DataFrame:
        area_all_emg_data = pd.DataFrame()

        for i, column in enumerate(data):
            area_emg_column_data = integrate.trapz(data[column].to_numpy())
            area_all_emg_data[data[column].name] = pd.Series(area_emg_column_data)

        return area_all_emg_data

    def _compute_mean_envelopes_by_emg(self) -> pd.DataFrame:
        mean_normalized_envelope_by_emg_data = pd.DataFrame()

        for column in self._dataframes[0].columns:
            sum = 0

            for i in range(len(self._dataframes)):
                sum += self._dataframes[i][column]

            mean_normalized_envelope_by_emg_data[column] = sum / len(self._dataframes)

        mean_normalized_envelope_by_emg_data.set_index(
            mean_normalized_envelope_by_emg_data.columns[0], inplace=True
        )

        return mean_normalized_envelope_by_emg_data

    def _write_data_file(
        self, data: dict | pd.DataFrame, file_type: str, prefix: Optional[str] = None
    ) -> None:
        if file_type == "JSON":
            ext = ".json"
        elif file_type == "CSV":
            ext = ".csv"
        else:
            raise ValueError("file_type argument must be JSON or CSV")

        if prefix is None:
            output_filename = f"{self._stage}{ext}"
        else:
            output_filename = f"{prefix}_{self._stage}{ext}"

        file_output_path = os.path.join(self._data_path, output_filename)

        if file_type == "JSON":
            try:
                with open(file_output_path, "w") as write_file:
                    json.dump(data, write_file)
            except Exception as error:
                raise Exception(
                    f"error occurs while trying to write areas in file: {self._data_path}. Reason: {error}"
                )
        elif file_type == "CSV":
            if type(data) is pd.DataFrame:
                data.to_csv(file_output_path, sep="\t", encoding="utf-8")
            else:
                raise TypeError(
                    f"data argument must be a DataFrame. Received: {type(data)}"
                )

    def get_areas(self) -> pd.DataFrame:
        json_areas_file_path = os.path.join(self._data_path, f"areas_{self._stage}.json")

        try:
            return pd.read_json(json_areas_file_path, encoding="utf-8")
        except pd.errors.ParserError as error:
            raise pd.errors.ParserError(error)

    def start_processing(self) -> dict:
        mean_normalized_envelope_by_emg_data = self._compute_mean_envelopes_by_emg()

        self._write_data_file(
            mean_normalized_envelope_by_emg_data, "CSV", prefix="envelopes"
        )

        mean_normalized_envelope_all_emg_data = (
            pd.concat(self._dataframes).groupby(level=0).mean()
        )

        area_mean_all_emg_data = self._compute_areas(
            mean_normalized_envelope_all_emg_data
        )

        areas = {}

        for i in range(len(self._dataframes)):
            iteration_area_data = self._compute_areas(self._dataframes[i])
            areas[f"iteration_{i}"] = iteration_area_data.to_dict(orient="records")[0]

        areas["mean"] = area_mean_all_emg_data.to_dict(orient="records")[0]

        self._write_data_file(areas, "JSON", prefix="areas")

        return areas
