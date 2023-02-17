import bcrypt
from flask_httpauth import HTTPTokenAuth

from configuration import Configuration
from src.api.utils import APIKey

auth = HTTPTokenAuth(header="X-API-Key")
api_key_hashed = APIKey.hash_key(Configuration.API_KEY.value)


@auth.verify_token
def verify_api_key(key) -> bool:
    return bcrypt.checkpw(key.encode("utf-8"), api_key_hashed)
