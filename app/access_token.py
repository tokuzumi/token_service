import time
import jwt

class VideoGrant(dict):
    def __init__(self, room_join=True, room=None):
        super().__init__()
        if room_join:
            self["roomJoin"] = True  # CORREÇÃO APLICADA AQUI
        if room:
            self["room"] = room

class AccessToken:
    def __init__(self, api_key, api_secret, identity, ttl=3600):
        self.api_key = api_key
        self.api_secret = api_secret
        self.identity = identity
        self.ttl = ttl
        self.grants = {}

    def add_grant(self, grant):
        self.grants.update(grant)

    def to_jwt(self):
        now = int(time.time())
        payload = {
            "iss": self.api_key,
            "sub": self.identity,
            "nbf": now,
            "exp": now + self.ttl,
            "video": self.grants,
        }
        return jwt.encode(payload, self.api_secret, algorithm="HS256")
