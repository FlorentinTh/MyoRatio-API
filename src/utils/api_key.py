import bcrypt


class APIKey:
    @staticmethod
    def hash_key(key):
        key_bytes = key.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(key_bytes, salt)
