import bcrypt
from flask_httpauth import HTTPTokenAuth

from myoratio.api import Configuration
from myoratio.api.utils import APIKey

configuration = Configuration.load()

auth = HTTPTokenAuth(header="X-API-Key")
api_key_hashed = APIKey.hash_key(str(configuration["API_KEY"]))


@auth.verify_token
def verify_api_key(key: str) -> bool:
    return bcrypt.checkpw(key.encode("utf-8"), api_key_hashed)
