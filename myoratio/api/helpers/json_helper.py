import json
import os


class JSONHelper:
    @staticmethod
    def read_participants_metadata(metadata_analysis_path: str) -> list:
        participants = []

        try:
            metadata_file = open(
                os.path.join(metadata_analysis_path, "data.json"),
                mode="r",
                encoding="utf-8",
            )

            metadata = json.load(metadata_file)

            metadata_file.close()
        except Exception as error:
            raise Exception(
                f"error occurs while trying to read participants metadata. Reason: {error}"
            )

        for participant in metadata.items():
            participants.append(participant)

        return participants
