# -*- coding: UTF-8 -*-
import requests

def post_form(*args, **kwargs) -> dict:
    """A post request with a payload content type of x-www-form-urlencoded format"""
    # request url api
    url = "https://xxxxxxxx/xx/xx"
    
    # request header
    headers = {
        'Authorization': 'Bearer xxxxxxxxxxxx',
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    
    # request body
    body = {
        'msg_id': '000001',
        'content': 'hello world!',
        'msg_type': 'text'
    }
    payload_form = lambda data: "&".join([f"{i[0]}={i[1]}" for i in data.items()])
    payload = payload_form(body)
    
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
    ret = post_form()
    print(ret)
