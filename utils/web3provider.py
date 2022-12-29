import json

from web3 import Web3

ganache_url = 'http://127.0.0.1:8545'


def get_provider():
    return Web3Provider.web3


class Web3Provider:
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    sharifstarter_contract_address = '0xFdB17de4fAa5A112b70B5F6f911b498c2FdA85A9'

    @staticmethod
    def create_eth_account(password):
        account = Web3Provider.web3.eth.account.create()
        return account.address, account.encrypt(password)

    @staticmethod
    def get_project(address):
        f = open('contract/Project.json')
        project_abi = json.load(f)
        address = Web3Provider.web3.toChecksumAddress(address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=project_abi)
        return contract

    @staticmethod
    def get_auction(address):
        f = open('contract/Auction.json')
        project_abi = json.load(f)
        address = Web3Provider.web3.toChecksumAddress(address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=project_abi)
        return contract

    @staticmethod
    def get_sharif_starter():
        f = open('contract/SharifStarter.json')
        sharifstarter_abi = json.load(f)
        address = Web3Provider.web3.toChecksumAddress(Web3Provider.sharifstarter_contract_address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=sharifstarter_abi)
        return contract
