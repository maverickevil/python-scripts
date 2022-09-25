# -*- coding: UTF-8 -*-
from ldap3 import Server, Connection, SUBTREE, ALL, NTLM
import json

server_ip = '192.168.0.1'
login_user = 'admin'
login_pass = 'abcde@123'
dn_group = 'CN=xxx,OU=xxx,DC=xxx,DC=xxx'


class Search_AD_Member(object):
    def __init__(self, **kwargs):
        self.ipaddr = kwargs.get('server_ip')
        self.user = kwargs.get('login_user')
        self.passwd = kwargs.get('login_pass')
        self.dn = kwargs.get('dn_group')

    def __connect_ad(self):
        """Connect to AD with SSL"""
        conn = None
        try:
            server = Server(self.ipaddr, get_info=ALL, use_ssl=False)
            conn = Connection(server,
                              user=self.user,
                              password=self.passwd,
                              auto_bind=True,
                              authentication=NTLM)
        except Exception as e:
            if conn:
                conn.unbind()
            raise Exception(f"\nIP: {self.ipaddr}, USER: {self.user}, PASSWD: {self.passwd}\nREASON: {e}")
        return conn

    @property
    def search_info(self) -> dict:
        """List group dn info"""
        conn = self.__connect_ad()
        conn.search(search_base=self.dn,
                    search_filter='(objectClass=*)',
                    attributes=['*'],
                    search_scope=SUBTREE,
                    size_limit=0)
        json_data = conn.response_to_json()
        conn.unbind()
        return json.loads(json_data)


def main():
    conn_dict = {
        'server_ip': server_ip,
        'login_user': login_user,
        'login_pass': login_pass,
        'dn_group': dn_group
    }
    s = Search_AD_Member(**conn_dict)
    data = s.search_info
    members = data.get('entries')[0].get('attributes').get('member')
    print(members)


if __name__ == '__main__':
    main()

