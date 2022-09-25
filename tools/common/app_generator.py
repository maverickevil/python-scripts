import time
import uuid
import base64
import random
import string
import hashlib


class AppTickets:
    def __init__(self):
        self.app_id = 'cli_' + ''.join(random.sample(string.ascii_lowercase + string.digits, 16))
        self.app_secret = ''.join(random.sample(string.ascii_letters + string.digits, 32))

    def __dict__(self):
        """
        app_id: cli_[16位随机字符串]  范围: a-z0-9
        app_secret: [32位随机字符串]  范围: a-zA-Z0-9
        """
        return {
            'app_id': self.app_id,
            'app_secret': self.app_secret,
        }

    def __str__(self):
        """
        token_str: t-[随机token字符串]
        """
        token_str = 't-' + base64.b64encode(bytes(str(uuid.uuid4()), 'utf-8')).decode('utf-8').lower()
        return token_str

    def __call__(self, *args, **kwargs):
        """
        username: $sign$[app_id]$[timestamp]
        password: sha256([app_secret][timestamp])
        """
        timestamp = str(time.time())
        username = f'$sign${self.app_id}${timestamp}'
        seed = self.app_secret + timestamp
        password = hashlib.sha256(seed.encode('utf-8')).hexdigest()
        return username, password


if __name__ == '__main__':
    app = AppTickets()
    print(app)               # t-odjiztmwngutztqzmi00mmexlwixzmqtnzi1zjg4yjbjmmy1
    print(app())             # ('$sign$cli_bjcxukhgr532fon8$1660661496.256507', '6b3d75b61bd21089f6f888184480f588d09e33ee712624aa00bf20fda84c2fe0')
    print(app.__dict__())    # {'app_id': 'cli_bjcxukhgr532fon8', 'app_secret': 'rOZJ0eG1kf5lxuhQvEj9NmPS3YWzdisb'}
