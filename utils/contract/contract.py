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



contract_address = '0x076EF90134101b93c3720d9E75EB0C4aF0Aa7752'


def get_sharif_starter():
    sharifstarter_abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{'
        '"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256",'
        '"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{'
        '"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,'
        '"internalType":"address","name":"projectStarter","type":"address"},{"indexed":false,"internalType":"string",'
        '"name":"name","type":"string"},{"indexed":false,"internalType":"string","name":"symbol","type":"string"},'
        '{"indexed":false,"internalType":"string","name":"description","type":"string"},{"indexed":false,'
        '"internalType":"uint256","name":"totalSupply","type":"uint256"}],"name":"ProjectCreated","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{'
        '"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender",'
        '"type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"contract Project","name":"project","type":"address"}],"name":"approveProject",'
        '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],'
        '"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharifstarter",'
        '"type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string",'
        '"name":"symbol","type":"string"},{"internalType":"string","name":"description","type":"string"},'
        '{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"name":"createProject","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{'
        '"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool",'
        '"name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"string","name":"symbol","type":"string"}],"name":"getProjectBySymbol","outputs":[{'
        '"internalType":"contract Project","name":"","type":"address"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"getProjects","outputs":[{"internalType":"contract Project[]","name":"","type":"address['
        ']"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],'
        '"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":['
        '],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],'
        '"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from",'
        '"type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
    address = web3.toChecksumAddress(contract_address)
    contract = web3.eth.contract(address=address, abi=sharifstarter_abi)
    return contract


def deploy_project_contract(address):
    web3.eth.defaultAccount = web3.eth.accounts[0]
    contract = get_sharif_starter()
    print(contract.functions.symbol().call())

    tx_hash = contract.functions.createProject(contract.address, 'ProjectTest1', 'PT1', 'description', 20000).transact()

    print(tx_hash)
    # Wait for transaction to be mined
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)

    event = contract.events.ProjectCreated().processReceipt(receipt)
    return event[0]['args']


def get_project_by_contract(address):
    project_abi = json.loads(
        '[{"inputs":[{"internalType":"address","name":"sharifstarter","type":"address"},{"internalType":"address",'
        '"name":"founder","type":"address"},{"internalType":"string","name":"name","type":"string"},'
        '{"internalType":"string","name":"symbol","type":"string"},{"internalType":"string","name":"description",'
        '"type":"string"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],'
        '"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value",'
        '"type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],'
        '"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},'
        '{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"approveProject",'
        '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"}],"name":"auctions","outputs":[{"internalType":"contract Auction","name":"",'
        '"type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"canelProject",'
        '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"biddingTime","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},'
        '{"internalType":"uint256","name":"minimumBid","type":"uint256"}],"name":"createAuction","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],'
        '"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"fundProject","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAuctions","outputs":[{'
        '"internalType":"contract Auction[]","name":"","type":"address[]"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},'
        '{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"isApprovedForCrowdFund","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string",'
        '"name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],'
        '"name":"projectDetails","outputs":[{"internalType":"address","name":"founder","type":"address"},'
        '{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol",'
        '"type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256",'
        '"name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],'
        '"name":"releaseProject","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"name":"shareHolders","outputs":[{'
        '"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"stage","outputs":[{"internalType":"enum DevelopmentStages","name":"","type":"uint8"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":['
        '],"name":"tempAddress","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},'
        '{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
    address = web3.toChecksumAddress(address)
    contract = web3.eth.contract(address=address, abi=project_abi)
    return contract

