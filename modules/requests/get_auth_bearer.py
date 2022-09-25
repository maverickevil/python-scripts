# -*- coding: UTF-8 -*-
import requests

def get_req(*args, **kwargs) -> dict:
    """normal get request"""
    # request url api
    url = "https://xxxxxxxx/xx/xx"
    
    # query params
    query_params = {
        'user_id': '000001',
        'page_size': 100
    }
    
    # request header
    headers = {
        'Authorization': 'Bearer xxxxxxxxxxxx',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # method get request
    response = requests.request(
        method="GET",
        url=url,
        params=query_params,
        headers=headers
    )
    
    # response
    if resp.status_code == 200:
        ret = resp.json().get('xxx')
        return ret
    return resp


if __name__ == '__main__':
    ret = get_req()
    print(ret)
