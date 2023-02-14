import os


class FileHelper:
    @staticmethod
    def get_participant_metadata_folder(base_path: str, csv_path: tuple) -> str:
        split_path = csv_path[0].split(os.sep)
        analysis = split_path[len(split_path) - 2]
        participant = split_path[len(split_path) - 1]
        return os.path.join(base_path, "analysis", ".metadata", analysis, participant)
