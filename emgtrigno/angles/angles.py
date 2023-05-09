import os
from typing import Optional

import pandas as pd

from emgtrigno.api.helpers import JSONHelper, PathHelper, StringHelper


class Angles:
    def __init__(self, data_path: str) -> None:
        self._data_path = data_path

    def _compute_mean_angles(self, dataframes: list[pd.DataFrame]) -> pd.DataFrame:
        mean_angles = pd.DataFrame()

        for column in dataframes[0].columns:
            sum = 0

            for i in range(len(dataframes)):
                sum += dataframes[i][column]

            mean_angles[column] = sum / len(dataframes)

        mean_angles.set_index(mean_angles.columns[0], inplace=True)
        return mean_angles

    def _write_mean_angles(self, data: pd.DataFrame) -> None:
        csv_output_filename = f"angles.csv"
        csv_file_output_path = os.path.join(self._data_path, csv_output_filename)
        data.to_csv(csv_file_output_path, sep="\t", encoding="utf-8")

    def get_angles_data(
        self, csv_path: tuple[str, str], prefix: Optional[str] = None
    ) -> pd.DataFrame:
        csv_angles_file_path = PathHelper.get_angles_csv_file_path(
            self._data_path, csv_path, prefix
        )
        try:
            return pd.read_csv(
                csv_angles_file_path, sep="\t", encoding="utf-8", engine="c"
            )
        except pd.errors.ParserError as error:
            raise pd.errors.ParserError(error)

    def get_mean_angles_data(self) -> pd.DataFrame:
        csv_angles_file_path = os.path.join(self._data_path, "angles.csv")

        try:
            return pd.read_csv(
                csv_angles_file_path, sep="\t", encoding="utf-8", engine="c"
            )
        except pd.errors.ParserError as error:
            raise pd.errors.ParserError(error)

    def get_angles_from_metadata(self, stage: str) -> list[dict[str, dict[str, float]]]:
        directory_path, participant = os.path.split(self._data_path)
        participants = JSONHelper.read_participants_metadata(directory_path)
        participant_key = StringHelper.format_participant_name_as_json_key(participant)

        participant_metadata = {}

        for participant in participants:
            if participant[0] == participant_key:
                participant_metadata = participant[1]

        if not bool(participant_metadata):
            raise ValueError(
                f"cannot find a valid participant in provided path: {self._data_path}"
            )

        stage_obj = participant_metadata["stages"][stage]

        points_values = []

        if stage_obj["completed"] is True:
            iterations = stage_obj["iterations"]

            for i in iterations:
                points = iterations[i]["points"]
                is_auto = True

                for j in points["auto"]:
                    if points["auto"][j]["x"] is None:
                        is_auto = False
                        break

                data = points["auto"] if is_auto else points["manual"]
                points_values.append(data)

        return points_values

    def start_processing(self, csv_files: list[str]) -> None:
        dataframes = []

        for csv_file in csv_files:
            try:
                dataframe = pd.read_csv(csv_file, sep="\t", encoding="utf-8", engine="c")
                dataframe.set_index(dataframe.columns[0], inplace=True)
                dataframes.append(dataframe)
            except pd.errors.ParserError as error:
                raise pd.errors.ParserError(error)

        mean_angles = self._compute_mean_angles(dataframes)
        self._write_mean_angles(mean_angles)
