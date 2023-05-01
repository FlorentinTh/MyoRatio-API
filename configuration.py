from enum import Enum


class Configuration(Enum):
    HOST = "127.0.0.1"
    # deepcode ignore HardcodedNonCryptoSecret: both GUI and API are running locally anyway
    API_KEY = "c5cd556a0983"
