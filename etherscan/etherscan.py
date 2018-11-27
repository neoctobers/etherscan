# coding:utf-8
import requests


class Client():

    def __init__(self,
                 api_key: str,
                 network=None,
                 ):

        # API URL
        self._api_url = 'https://api.etherscan.io/api'

        # API Key
        self._api_key = api_key

        # Network
        if network:
            if network not in ['ropsten', 'kovan', 'rinkeby']:
                raise Exception('network could only be None(mainnet) /ropsten/kovan/rinkeby')

            self._api_url = 'https://api-{network}.etherscan.io/api'.format(
                network=network
            )

        # params
        self._params = {
            'apikey': self._api_key,
        }

    def _req(self):
        r = requests.post(url=self._api_url, data=self._params).json()

        if '1' == r['status']:
            return r['result']
        else:
            # todo: handle errors
            print(r)

        return r

    def _proxy_req(self):
        self._params['module'] = 'proxy'

        # get, json
        r = requests.get(url=self._api_url, data=self._params).json()

        # todo: handle exceptions

        return r['result']

    def get_eth_price(self):
        self._params['module'] = 'stats'
        self._params['action'] = 'ethprice'

        r = self._req()

        return {
            'ethbtc': float(r['ethbtc']),
            'ethbtc_timestamp': int(r['ethbtc_timestamp']),
            'ethusd': float(r['ethusd']),
            'ethusd_timestamp': int(r['ethbtc_timestamp']),
        }

    def get_eth_supply(self):
        self._params['module'] = 'stats'
        self._params['action'] = 'ethsupply'

        return int(self._req())

    def get_eth_balance(self, address: str):
        self._params['module'] = 'account'
        self._params['action'] = 'balance'
        self._params['address'] = address

        return int(self._req())

    def get_eth_balances(self, addresses: list):
        self._params['module'] = 'account'
        self._params['action'] = 'balancemulti'
        self._params['address'] = ','.join(addresses)

        balances = {}
        for row in self._req():
            balances[row['account']] = int(row['balance'])

        return balances

    def get_gas_price(self):
        self._params['action'] = 'eth_gasPrice'

        return int(self._proxy_req(), 16)
