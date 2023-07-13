import os
import sys

from dotenv import dotenv_values
from simple_schema_validator import schema_validator


class Configuration:
    @staticmethod
    def load() -> dict:
        schema = {"HOST": str, "API_KEY": str}
        data_directory = ""

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            data_directory = sys._MEIPASS  # type: ignore

        configuration = dotenv_values(dotenv_path=os.path.join(data_directory, ".env"))
        validation = schema_validator(schema, configuration)

        if validation is not None:
            raise ValueError("Configuration file is not valid")

        return configuration
