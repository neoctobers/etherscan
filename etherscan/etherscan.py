# coding:utf-8
import requests


class Client():

    def __init__(self,
                 api_key: str,
                 network='mainnet',
                 ):
        if network not in ['mainnet', 'ropsten', 'kovan', 'rinkeby']:
            raise Exception('network could only be mainnet/ropsten/kovan/rinkeby')

        self._api_key = api_key

        # Base URL
        self._base_url = 'https://api.etherscan.io/api?'

        # Endpoint URL
        self._endpoint = 'https://api.etherscan.io/api?'

        # # headers
        # self._headers = {
        #     'Content-Type': 'application/json',
        # }
        #
        # # params
        # self._params = []
        #
        # # payload
        # self._payload = {
        #     'jsonrpc': '2.0',
        #     'id': 1,
        # }

    def req(self):
        # self._payload['params'] = self._params

        r = requests.get(
            url=self._endpoint,
        ).json()

        if '1' == r['status']:
            return r['result']

        # todo: handle with error
        return r

    def get_eth_price(self):
        self._endpoint = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={}'.format(self._api_key)

        return self.req()

