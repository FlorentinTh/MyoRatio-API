import os

import pandas as pd

from .file_helper import FileHelper


class CSVHelper:
    @staticmethod
    def write_normalized_envelope(base_path: str, csv_path, stage: str, data: pd.DataFrame) -> None:
        csv_output_filename = f'envelope_{stage}_{os.path.splitext(csv_path[1])[0]}.csv'
        participant_metadata_folder = FileHelper.get_participant_metadata_folder(base_path, csv_path)
        csv_file_output_path = os.path.join(participant_metadata_folder, csv_output_filename)
        data.to_csv(csv_file_output_path, sep='\t', encoding='utf-8')
