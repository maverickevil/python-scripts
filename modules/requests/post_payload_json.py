# -*- coding: UTF-8 -*-
import requests
import json

def post_json(*args, **kwargs) -> dict:
    """The post request with the payload in json format"""
    # request url api
    url = "https://xxxxxxxx/xx/xx"

    # request header
    headers = {
        'Authorization': 'Token xxxxxxxxxxxx',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # request body
    body = {
        'msg_id': '000001',
        'content': 'hello world!',
        'msg_type': 'text'
    }
    payload = json.dumps(body)
    
    # method post request
    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        data=payload
    )
    
    # response
    if resp.status_code == 200:
        ret = resp.json().get('xxx')
        return ret
    return resp


if __name__ == '__main__':
    ret = post_json()
    print(ret)
