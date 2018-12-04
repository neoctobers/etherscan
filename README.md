# Etherscan.io API wrapper

[![PyPi Version](http://img.shields.io/pypi/v/etherscan.svg)](https://pypi.python.org/pypi/etherscan/)

An Etherscan.io API wrapper, for Python.

With a default cache supported by [requests-cache](https://github.com/reclosedev/requests-cache)

## Installation
```
pip3 install etherscan
```

## Usage
```python
import etherscan

es = etherscan.Client(
    api_key='YOUR_API_KEY',
    cache_expire_after=5,
)

eth_price = es.get_eth_price()

eth_supply = es.get_eth_supply()

eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')

eth_balances = es.get_eth_balances([
    '0x39eB410144784010b84B076087B073889411F878',
    '0x39eB410144784010b84B076087B073889411F879',
])

gas_price = es.get_gas_price()

block = es.get_block_by_number(block_number=12345)

transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')

token_transations = es.get_token_transactions(
    contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
    address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
)
```
