import os


class FileHelper:
    @staticmethod
    def get_analysis_base_folder_path(base_path: str) -> str:
        return os.path.join(base_path, "analysis")

    @staticmethod
    def get_analysis_folder_path(base_path: str, analysis: str) -> str:
        return os.path.join(FileHelper.get_analysis_base_folder_path(base_path), analysis)

    @staticmethod
    def get_metadata_analysis_path(base_path: str, analysis: str) -> str:
        return os.path.join(
            FileHelper.get_analysis_base_folder_path(base_path), ".metadata", analysis
        )

    @staticmethod
    def get_participant_metadata_folder(base_path: str, csv_path: tuple) -> str:
        split_path = csv_path[0].split(os.sep)
        analysis = split_path[len(split_path) - 2]
        participant = split_path[len(split_path) - 1]
        return os.path.join(
            FileHelper.get_metadata_analysis_path(base_path, analysis), participant
        )
