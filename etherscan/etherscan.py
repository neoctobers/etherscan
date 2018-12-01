# coding:utf-8
import os
import tempfile
import requests_cache


class Client():

    def __init__(self,
                 api_key: str,
                 network=None,
                 cache_backend='sqlite',
                 cache_expire_after=3,
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

        # session & cache
        self._session = None
        self._cache_name = os.path.join(tempfile.gettempdir(), 'etherscan_cache')
        self._cache_backend = cache_backend
        self._cache_expire_after = cache_expire_after

    @property
    def session(self):
        if not self._session:
            self._session = requests_cache.core.CachedSession(
                cache_name=self._cache_name,
                backend=self._cache_backend,
                expire_after=self._cache_expire_after,
            )
            self._session.headers.update(
                {
                    'User-agent': 'etherscan - python wrapper '
                                  'around etherscan.io (github.com/neoctobers/etherscan)'
                }
            )
        return self._session

    def __req(self):
        r = self.session.post(url=self._api_url, data=self._params).json()

        if '1' == r['status']:
            return r['result']
        else:
            # todo: handle errors
            print(r)

        return r

    def __proxy_req(self):
        self._params['module'] = 'proxy'

        # get, json
        r = self.session.get(url=self._api_url, data=self._params).json()

        # todo: handle exceptions

        return r['result']

    def get_eth_price(self):
        self._params['module'] = 'stats'
        self._params['action'] = 'ethprice'

        r = self.__req()

        return {
            'ethbtc': float(r['ethbtc']),
            'ethbtc_timestamp': int(r['ethbtc_timestamp']),
            'ethusd': float(r['ethusd']),
            'ethusd_timestamp': int(r['ethbtc_timestamp']),
        }

    def get_eth_supply(self):
        self._params['module'] = 'stats'
        self._params['action'] = 'ethsupply'

        return int(self.__req())

    def get_eth_balance(self, address: str):
        self._params['module'] = 'account'
        self._params['action'] = 'balance'
        self._params['address'] = address

        return int(self.__req())

    def get_eth_balances(self, addresses: list):
        self._params['module'] = 'account'
        self._params['action'] = 'balancemulti'
        self._params['address'] = ','.join(addresses)

        balances = {}
        for row in self.__req():
            balances[row['account']] = int(row['balance'])

        return balances

    def get_gas_price(self):
        self._params['action'] = 'eth_gasPrice'

        return int(self.__proxy_req(), 16)

    def get_block_number(self):
        self._params['action'] = 'eth_blockNumber'

        return int(self.__proxy_req(), 16)

    def get_block_by_number(self, block_number):
        self._params['action'] = 'eth_getBlockByNumber'
        self._params['tag'] = hex(block_number)
        self._params['boolean'] = True

        return self.__proxy_req()
