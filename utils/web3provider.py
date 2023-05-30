import json

from web3 import Web3


ganache_url = 'http://127.0.0.1:8545'


def get_provider():
    if Web3Provider.web3.isConnected():
        return Web3Provider
    return None


class Web3Provider:
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    sharifstarter_contract_address = '0x504695d677eaf67168Dc467743afbC3D541b1f55'
    manager = '0x4d56C6784587455b845718c392A66F104A2bA3bD'
    manager_pass = '6cc8f3ca777f4838c9e13811bbba48b7de749e88e4540cecc4b04b965d098a88'
    @staticmethod
    def create_eth_account(password):
        account = Web3Provider.web3.eth.account.create()
        return account.address, account.encrypt(password)

    @staticmethod
    def get_project(address):
        f = open('contract/Project.abi')
        project_abi = f.read()
        address = Web3Provider.web3.toChecksumAddress(address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=project_abi)
        return contract

    @staticmethod
    def get_auction(address):
        f = open('contract/Auction.abi')
        project_abi = f.read()
        address = Web3Provider.web3.toChecksumAddress(address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=project_abi)
        return contract

    @staticmethod
    def get_sharif_starter():
        f = open('contract/SharifStarter.abi')
        sharifstarter_abi = f.read()
        address = Web3Provider.web3.toChecksumAddress(Web3Provider.sharifstarter_contract_address)
        contract = Web3Provider.web3.eth.contract(address=address, abi=sharifstarter_abi)
        return contract

    @staticmethod
    async def deploy_project_contract(creator,encrypted_private_key,password,name,symbol,desc,total):
        contract = Web3Provider.get_sharif_starter()
        print(contract.functions.symbol().call())
        func = contract.functions.createProject(Web3Provider.manager,name ,symbol ,desc ,total)

        transaction = {
            "gasPrice": Web3Provider.web3.eth.gas_price,
            "from" : creator
        }
        privateKey = Web3Provider.web3.eth.account.decrypt(json.loads(encrypted_private_key),password)
        txn = func.buildTransaction(transaction)
        signed = Web3Provider.web3.eth.account.signTransaction(txn, privateKey)
        txn_hash = Web3Provider.web3.eth.sendRawTransaction(signed.rawTransaction)

        # Wait for transaction to be mined
        receipt = Web3Provider.web3.eth.waitForTransactionReceipt(txn_hash)
        print(receipt)

        event = contract.events.ProjectCreated().processReceipt(receipt)
        return event[0]['args']