import os
import json

from .file_helper import FileHelper


class JSONHelper:
    @staticmethod
    def write_angle_file(base_path, csv_path, data, prefix=None):
        data.rename(columns={f'{data.columns[0]}': 'x'}, inplace=True)

        if prefix is None:
            json_output_filename = f'angle_{os.path.splitext(csv_path[1])[0]}.json'
        else:
            json_output_filename = f'{prefix}_angle_{os.path.splitext(csv_path[1])[0]}.json'

        participant_metadata_folder = FileHelper.get_participant_metadata_folder(base_path, csv_path)
        json_file_output_path = os.path.join(participant_metadata_folder, json_output_filename)
        data.to_json(json_file_output_path, orient='records')

    @staticmethod
    def write_areas_file(data_path, data):
        path = os.path.join(data_path, 'areas.json')
        with open(path, "w") as write_file:
            json.dump(data, write_file)
