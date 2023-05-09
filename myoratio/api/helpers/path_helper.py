import os
from typing import Optional


class PathHelper:
    @staticmethod
    def get_root_module_path() -> str:
        return os.path.abspath(os.curdir)

    @staticmethod
    def get_analysis_base_folder_path(base_path: str) -> str:
        return os.path.join(base_path, "analysis")

    @staticmethod
    def get_analysis_folder_path(base_path: str, analysis: str) -> str:
        return os.path.join(PathHelper.get_analysis_base_folder_path(base_path), analysis)

    @staticmethod
    def get_metadata_analysis_path(base_path: str, analysis: str) -> str:
        return os.path.join(
            PathHelper.get_analysis_base_folder_path(base_path), ".metadata", analysis
        )

    @staticmethod
    def get_participant_metadata_folder(base_path: str, csv_path: tuple[str, str]) -> str:
        split_path = csv_path[0].split(os.sep)
        analysis = split_path[len(split_path) - 2]
        participant = split_path[len(split_path) - 1]

        return os.path.join(
            PathHelper.get_metadata_analysis_path(base_path, analysis), participant
        )

    @staticmethod
    def get_angles_csv_file_path(
        base_path: str, csv_path: tuple[str, str], prefix: Optional[str] = None
    ) -> str:
        if prefix is None:
            csv_filename = csv_path[1]
        else:
            csv_filename = f"{prefix}_angle_{csv_path[1]}"

        participant_metadata_folder = PathHelper.get_participant_metadata_folder(
            base_path, csv_path
        )

        return os.path.join(participant_metadata_folder, csv_filename)
