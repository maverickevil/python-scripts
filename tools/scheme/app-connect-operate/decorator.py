# -*- coding: UTF-8 -*-
from ldap3 import Server, Connection, SUBTREE, ALL, NTLM
import json

server_ip = '192.168.0.1'
login_user = 'admin'
login_pass = 'abcde@123'
dn_group = 'CN=xxx,OU=xxx,DC=xxx,DC=xxx'


def conn(ipaddr, user, passwd):
    def connect_ad(func):
        """Connect to AD with SSL"""
        def inner(*args, **kwargs):
            server = Server(ipaddr, get_info=ALL, use_ssl=False)
            conn = Connection(server, user=user, password=passwd, auto_bind=True, authentication=NTLM)
            res = func(conn, kwargs['dn'])
            return res
        return inner
    return connect_ad


@conn(ipaddr=server_ip, user=login_user, passwd=login_pass)
def search_dn_info(conn, dn) -> dict:
    """List group dn info"""
    conn.search(search_base=dn, search_filter='(objectClass=*)', attributes=['*'], search_scope=SUBTREE, size_limit=0)
    json_data = conn.response_to_json()
    conn.unbind()
    return json.loads(json_data)


def main():
    data = search_dn_info(conn, dn=dn_group)
    members = data.get('entries')[0].get('attributes').get('member')
    print(members)


if __name__ == '__main__':
    main()

