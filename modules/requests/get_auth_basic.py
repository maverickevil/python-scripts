# -*- coding: UTF-8 -*-
from requests.auth import HTTPBasicAuth
import requests

def auth_get_req(*args, **kwargs) -> dict:
    """Authentication using Http Basic Authorization"""
    # request url api
    url = "https://xxxxxxxx/xx/xx"

    # query params
    query_params = {
        'user_id': '000001',
        'page_size': 100
    }

    # request header
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    # Attaches HTTP Basic Authentication to the given Request object.
    basic = HTTPBasicAuth('user', 'password')

    # method get request
    response = requests.request(
        method="GET",
        url=url,
        params=query_params,
        headers=headers,
        auth=basic
    )

    # response
    if resp.status_code == 200:
        ret = resp.json().get('xxx')
        return ret
    return resp


if __name__ == '__main__':
    ret = auth_get_req()
    print(ret)
