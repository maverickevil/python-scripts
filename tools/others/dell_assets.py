from collections import Counter
from typing import Dict
import requests
import re
import os


class DellWarranty(object):
    """
    [DELL TechDirect API] https://techdirect.dell.com/Portal/ManageAPI.aspx
    """
    instance = None

    client_info = {
        "client_id": os.getenv('CLIENT_ID'),
        "client_secret": os.getenv('CLIENT_SECRET')
        "grant_type": "client_credentials"
    }

    request_headers = {
        'Content-Type': None,
        'Authorization': None
    }

    def __new__(cls, *args, **kwargs):
        # singleton pattern
        if not cls.instance:
            cls.instance = object.__new__(cls)
        # print(cls.instance)
        # <__main__.DellWarranty object at 0x100a69df0>
        return cls.instance

    # [Obsolete]
    # Every time you run it, you need to instantiate the
    # method to get the token, which is unnecessary. It is
    # more efficient to use the singleton pattern.
    #
    # def __init__(self, **kwargs):
    #     self.client_id = kwargs['client_id']
    #     self.client_secret = kwargs['client_secret']
    #     self.grant_type = kwargs['grant_type']
    #     self.headers = self.access_token
    #
    # @property
    # def access_token(self) -> Dict:
    #     url = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"
    #     payload = {
    #         "client_id": self.client_id,
    #         "client_secret": self.client_secret,
    #         "grant_type": self.grant_type
    #     }
    #     response = requests.post(url=url, data=payload).json()
    #     self.headers.update({
    #         'Content-Type': 'application/json',
    #         'Authorization': "Bearer " + response.get('access_token')
    #     })
    #     return self.headers

    @classmethod
    def access_token(cls) -> None:
        url = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"
        cls_obj = eval(__class__.__name__)
        cls_obj.request_headers.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        payload = "&".join(["=".join(i) for i in cls.client_info.items()])
        response = requests.post(url=url, headers=cls.request_headers, data=payload).json()
        if response.get('token_type') != 'Bearer':
            raise ValueError('api token auth type not supported')
        bearer_token = "Bearer {0}".format(response.get('access_token'))
        cls_obj.request_headers.update({
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        })

    @classmethod
    def asset_summary(cls, sn: str) -> Dict:
        # Authentication: Singleton Pattern
        if cls.request_headers.get('Authorization') is None:
            cls.access_token()
        url = "https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlement-components"
        query_params = {
            'servicetag': sn
        }
        response = requests.get(url=url, params=query_params, headers=cls.request_headers)
        if response.status_code != 200:
            raise ValueError(response.text)
        json_data = response.json()
        return json_data

    @classmethod
    def gofmt(cls, sn: str) -> Dict:
        # initial
        cls.instance = __class__()
        data = cls.instance.asset_summary(sn)

        # basic
        product_number = data.get('productLineDescription').split()[-1].lower().replace('r', 'R')
        collects = {
            'serial_number': data.get('serviceTag'),
            'product_number': product_number,
            'product_model': 'PowerEdge {model}'.format(model=product_number)
        }

        # entitlements
        entitlements = data.get('entitlements')
        if not entitlements:
            raise ValueError('dell service warranty is empty')
        highest_service_level = entitlements[0]
        service_level = {
            'start_date': highest_service_level.get('startDate'),
            'end_date': highest_service_level.get('endDate'),
            'sl_code': highest_service_level.get('serviceLevelCode'),
            'sl_desc': highest_service_level.get('serviceLevelDescription')
        }
        collects.update({
            'service_level': service_level
        })

        # components
        components = data.get('components')

        product_specs = ""
        # CPU/DIMM/SSD/RAID/NIC/SFP+/PowerSupply/ReadyRails/iDRAC License
        for item in components:
            text = item.get('partDescription')
            match = re.search(
                r'PRC,\d+.*\d+MB,CLX|PRC,.*G,IRKL|PRC,.*G,ICX|PRC,.*M|DIMM,\d+GB|Solid State Drive|HD,\dTB|SSDR,.*T|SAS-SATAU|ADPT,SAS-RAID|INFO,.*MSTNR|INFO,C\d|INTEL.*MISC|SFP\+,\d+G,SR|PWR SPLY,\d+W,|KIT,RCKRL,1U|KIT,RCKRL|SRV,LICENSE ENTITLEMENT|Intel|RAID Controller|SSD SATA|RDIMM,|Power Supply',
                text)
            if match:
                desc = item.get('itemDescription')
                count = item.get('partQuantity')
                info = f"'{desc}' * {count}; "
                product_specs += info
        
        components = [i.get('itemDescription') for i in components]
        counter = Counter(components)

        product_comps = ""
        for item in counter:
            match = re.search(r'Intel|RAID Controller|SSD SATA|RDIMM,|Power Supply', item)
            if match:
                product_comps += item
                product_comps += "; \n"

        collects.update({
            'components': product_comps,
            'specification': product_specs
        })
        return collects


if __name__ == '__main__':
    res1 = DellWarranty.gofmt('6F***83')
    print(res1)
    res2 = DellWarranty.gofmt('42***M3')
    print(res2)

"""
{
     "serial_number": "42***M3",
     "product_number": "R450",
     "product_model": "PowerEdge R450",
     "service_level": {
          "start_date": "2022-01-09T16:00:00Z",
          "end_date": "2025-01-10T15:59:59.000001Z",
          "sl_code": "PQ",
          "sl_desc": "4 Hour ProSupport Plus Mission Critical"
     },
     "components": "Intel Xeon Silver 4314 2.4G, 16C/32T, 10.4GT/s, 24M Cache, Turbo, HT (135W) DDR4-2666; \n32GB RDIMM, 3200MT/s, Dual Rank 16Gb BASE x8; \n1.92TB SSD SATA Mix Use 6Gbps 512 2.5in Hot-plug AG Drive,3.5in HYB CARR, 3 DWPD,; \nIntel X710 Dual Port 10GbE SFP+, OCP NIC 3.0; \n",
     "specification": "'Intel Xeon Silver 4314 2.4G, 16C/32T, 10.4GT/s, 24M Cache, Turbo, HT (135W) DDR4-2666' * 2; '32GB RDIMM, 3200MT/s, Dual Rank 16Gb BASE x8' * 2; '1.92TB SSD SATA Mix Use 6Gbps 512 2.5in Hot-plug AG Drive,3.5in HYB CARR, 3 DWPD,' * 2; 'RAID 1' * 1; 'Intel X710 Dual Port 10GbE SFP+, OCP NIC 3.0' * 1; 'Dell EMC PowerEdge SFP+ SR Optic 10GbE 850nm' * 2; 'Dual, Hot-plug, PSU (1+1), 800, Mixed Mode' * 2; 'ReadyRails Sliding Rails Without Cable Management Arm' * 1; 'iDRAC9, Enterprise 15G' * 1; "
}
"""
