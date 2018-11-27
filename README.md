# Etherscan.io API wrapper

An Etherscan.io API wrapper, for Python.

## Installation
```
pip3 install etherscan
```

## Usage
```python
import etherscan

es = etherscan.Client(
    api_key='YOUR_API_KEY',
)

eth_price = es.get_eth_price()

eth_supply = es.get_eth_supply()

eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')

eth_balances = es.get_eth_balances([
    '0x39eB410144784010b84B076087B073889411F878',
    '0x39eB410144784010b84B076087B073889411F879',
])

gas_price = es.get_gas_price()
```
