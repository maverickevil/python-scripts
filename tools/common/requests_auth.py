"""
Attaches HTTP Authentication to the given Request object.
Generate Basic/Bearer authentication token string.
"""

import requests.auth as auth


class AuthStr:
    _auth_str = None

    def __str__(self):
        return self._auth_str

    def __call__(self, r):
        r.headers["authorization"] = self.__str__()
        return r


class BearerAuth(auth.AuthBase, AuthStr):
    """Wrapping HTTP Bearer Authentication."""

    def __init__(self, token):
        self._auth_str = 'Bearer ' + str(token)


class BasicAuth(auth.AuthBase, AuthStr):
    """Wrapping HTTP Basic Authentication."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._auth_str = auth._basic_auth_str(self.username, self.password)


if __name__ == '__main__':
    basic_token = BasicAuth(username="admin", password="admin@12345")
    print(basic_token)      # Basic YWRtaW46YWRtaW5AMTIzNDU=

    bearer_token = BearerAuth("t-odjiztmwngutztqzmi00mmexlwixzmqtnzi1zjg4yjbjmmy1")
    print(bearer_token)     # Bearer t-odjiztmwngutztqzmi00mmexlwixzmqtnzi1zjg4yjbjmmy1
