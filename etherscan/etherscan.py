# coding:utf-8
import requests


class Client():

    def __init__(self,
                 api_key: str,
                 network=None,
                 ):

        # Base URL
        self._base_url = 'https://api.etherscan.io/api'

        # API Key
        self._api_key = api_key

        # Network
        if network:
            if network not in ['ropsten', 'kovan', 'rinkeby']:
                raise Exception('network could only be None(mainnet) /ropsten/kovan/rinkeby')

            self._base_url = 'https://api-{network}.etherscan.io/api'.format(
                network=network
            )

        # Endpoint URL
        self._url = self._base_url

        # params
        self._params = {
            'apikey': self._api_key,
        }

    def _update_url(self):
        # queries
        queries = []
        for key, value in self._params.items():
            queries.append('{key}={value}'.format(
                key=key,
                value=value,
            ))

        # url
        self._url = '{base_url}?{query_string}'.format(
            base_url=self._base_url,
            query_string='&'.join(queries)
        )

        return self._url

    def _req(self):
        self._update_url()

        # get, json
        r = requests.get(url=self._url).json()

        if '1' == r['status']:
            return r['result']
        else:
            # todo: handle errors
            print(r)

        return r

    def _proxy_req(self):
        self._params['module'] = 'proxy'
        self._update_url()

        # get, json
        r = requests.get(url=self._url).json()

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
