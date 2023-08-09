import os
import sys

from environs import Env
from simple_schema_validator import schema_validator


class Configuration:
    @staticmethod
    def load() -> dict:
        schema = {"HOST": str, "API_KEY": str}
        data_directory = ""

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            data_directory = sys._MEIPASS  # type: ignore

        env = Env()
        env.read_env(os.path.join(data_directory, ".env"), recurse=False)

        configuration = {
            "HOST": str(env("HOST")),
            "API_KEY": str(env("API_KEY")),
        }

        validation = schema_validator(schema, configuration)

        if not validation:
            raise ValueError("Configuration file is not valid")

        return configuration
