import json

from web3 import Web3

ganache_url = 'http://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())


def transaction(sender, receiver, private_key, amount):
    nonce = web3.eth.getTransactionCount(sender)
    # build a transaction
    tx = {
        'nonce': nonce,
        'to': receiver,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    # sign and send transaction
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    # return transaction hash
    return web3.toHex(tx_hash)


def get_balance(address):
    balance = web3.eth.getBalance(address)
    return web3.fromWei(balance, 'ether')






