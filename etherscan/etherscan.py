# coding:utf-8
import os
import tempfile
import requests_cache
from .errors import EtherscanIoException


class Client():

    def __init__(self,
                 api_key: str,
                 network=None,
                 cache_backend='sqlite',
                 cache_expire_after=5,
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

        if '0' == r['status']:
            print('--- Etherscan.io Message ---', r['message'])

        return r['result']

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

    def get_transactions_by_address(self,
                                    address: str,
                                    type: str = 'normal',
                                    start_block: int = 0,
                                    end_block: int = 999999999,
                                    page: int = 1,
                                    limit: int = 1000,
                                    sort: str = 'asc',
                                    ):

        self._params['module'] = 'account'

        if type == 'normal':
            self._params['action'] = 'txlist'
        elif type == 'internal':
            self._params['action'] = 'txlistinternal'
        else:
            raise Exception('param `type` must be "normal" or "internal"')

        self._params['address'] = address
        self._params['startblock'] = start_block
        self._params['endblock'] = end_block
        self._params['page'] = page
        self._params['offset'] = limit
        self._params['sort'] = sort

        return self.__req()

    def get_all_transactions_by_address(self,
                                        address: str,
                                        type: str = 'normal',
                                        limit_per_page: int = 1000,
                                        interval: float = 0.5,
                                        ):

        import time

        results = []

        page = 1
        while True:
            rs = self.get_transactions_by_address(address=address, type=type, page=page, limit=limit_per_page)
            if rs:
                results.extend(rs)
                page += 1
                time.sleep(interval)
            else:
                break

        return results

    def transaction(self, source: dict):
        """Repack the transaction dict"""

        r = {}

        r['timestamp'] = int(source['timeStamp'])

        r['from'] = source['from']
        r['to'] = source['to']
        r['input'] = source['input']
        r['hash'] = source['hash']
        r['value'] = int(source['value'])

        r['gas'] = int(source['gas'])
        r['gas_price'] = int(source['gasPrice'])
        r['gas_used'] = int(source['gasUsed'])
        r['nonce'] = int(source['nonce'])
        r['confirmations'] = int(source['confirmations'])

        r['block_number'] = int(source['blockNumber'])
        r['block_hash'] = source['blockHash']
        r['transaction_index'] = int(source['transactionIndex'])
        r['cumulative_gas_used'] = int(source['cumulativeGasUsed'])

        r['is_error'] = bool(source['isError'])
        r['tx_receipt_status'] = bool(source['txreceipt_status'])

        return r

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
