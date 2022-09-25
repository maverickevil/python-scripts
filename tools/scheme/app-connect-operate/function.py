# -*- coding: UTF-8 -*-
from ldap3 import Server, Connection, SUBTREE, ALL, NTLM
import json

server_ip = '192.168.0.1'
login_user = 'admin'
login_pass = 'abcde@123'
dn_group = 'CN=xxx,OU=xxx,DC=xxx,DC=xxx'


def connect_ad(ipaddr, user, passwd):
    """Connect to AD with SSL"""
    server = Server(ipaddr, get_info=ALL, use_ssl=False)
    conn = Connection(server, user=user, password=passwd, auto_bind=True, authentication=NTLM)
    return conn


def search_info(ipaddr, user, passwd, dn) -> dict:
    """List group dn info"""
    conn = connect_ad(ipaddr, user, passwd)
    conn.search(search_base=dn, search_filter='(objectClass=*)', attributes=['*'], search_scope=SUBTREE, size_limit=0)
    json_data = conn.response_to_json()
    conn.unbind()
    return json.loads(json_data)


def main():
    data = search_info(ipaddr=server_ip, user=login_user, passwd=login_pass, dn=dn_group)
    members = data.get('entries')[0].get('attributes').get('member')
    print(members)


if __name__ == '__main__':
    main()

