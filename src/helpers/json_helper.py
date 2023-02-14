import json
import os

import pandas as pd

from .file_helper import FileHelper


class JSONHelper:
    @staticmethod
    def write_angle_file(
        base_path: str, csv_path: tuple, data: pd.DataFrame, prefix: str = None
    ) -> None:
        data.rename(columns={f"{data.columns[0]}": "x"}, inplace=True)

        if prefix is None:
            json_output_filename = f"angle_{os.path.splitext(csv_path[1])[0]}.json"
        else:
            json_output_filename = (
                f"{prefix}_angle_{os.path.splitext(csv_path[1])[0]}.json"
            )

        participant_metadata_folder = FileHelper.get_participant_metadata_folder(
            base_path, csv_path
        )
        json_file_output_path = os.path.join(
            participant_metadata_folder, json_output_filename
        )
        data.to_json(json_file_output_path, orient="records")

    @staticmethod
    def write_ratio_file(
        data_path: str, stage: str, data: dict, suffix: str = None
    ) -> None:

        if suffix is None:
            path = os.path.join(data_path, f"ratios_{stage}_mean.json")
        else:
            path = os.path.join(data_path, f"ratios_{stage}_{suffix}.json")

        with open(path, "w") as write_file:
            json.dump(data, write_file)
