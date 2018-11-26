# coding:utf-8
import requests


class Client():

    def __init__(self,
                 api_key: str,
                 network='mainnet',
                 ):

        if network not in ['mainnet', 'ropsten', 'kovan', 'rinkeby']:
            raise Exception('network could only be mainnet/ropsten/kovan/rinkeby')

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

        # todo: handle with error
        # sample: {'jsonrpc': '2.0', 'id': 1, 'error': {'code': -32602, 'message': 'invalid argument 0: json: cannot unmarshal hex string of odd length into Go value of type common.Address'}}
        return r

