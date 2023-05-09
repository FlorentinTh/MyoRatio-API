class StringHelper:
    @staticmethod
    def format_participant_name_as_json_key(name: str) -> str:
        parts = name.split(" ")
        participant_id = parts[0]
        suffix = parts[1].lower().replace("(", "").replace(")", "")
        return f"participant_{participant_id}_{suffix}"

    @staticmethod
    def format_participant_name_as_folder_name(name: str) -> str:
        parts = name.split("_")
        participant_number = parts[1]
        letter = parts[2].upper()
        return f"{participant_number} ({letter})"

    @staticmethod
    def include_substring(string: str, substring: str) -> bool:
        if substring.lower() in string.lower():
            return True

        return False
