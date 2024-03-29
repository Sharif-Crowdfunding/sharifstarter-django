import json

from web3 import Web3

ganache_url = 'http://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())
print(web3.eth.accounts[0])


sharifstarter_contract_address = '0x504695d677eaf67168Dc467743afbC3D541b1f55'
manager= '0x4d56C6784587455b845718c392A66F104A2bA3bD'

def get_sharif_starter():
    f = open('SharifStarter.abi')
    sharifstarter_abi = f.read()
    address = web3.toChecksumAddress(sharifstarter_contract_address)
    contract = web3.eth.contract(address=address, abi=sharifstarter_abi)
    return contract


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

def transfer(self, sender, private_key, to, amount):
    nonce = self.web3.eth.getTransactionCount(sender)
    gas_estimate = self.contract_instance.functions.transfer(to, amount).estimateGas({'from': sender})
    print(f'Gas estimate to transact: {gas_estimate}')

    if gas_estimate < 100000:
        print("Sending transaction of transfer\n")
        tx_hash = self.contract_instance.functions.transfer(to, amount).buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': sender,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=private_key)
        print("signed tx")
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("tx sent")
        print("Transaction receipt mined:")
        print(sent_tx)
        print("\nWas transaction successful?")
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        print(result)
    else:
        print("Gas cost exceeds 100000")
def deploy_project_contract(creator, encrypted_private_key, password, name, symbol, desc, total):
    contract = get_sharif_starter()
    print(contract.functions.symbol().call())
    func = contract.functions.createProject(manager, name, symbol, desc, total)

    transaction = {
        "gasPrice": web3.eth.gas_price,
        'gas': 2000000,
        "from": creator
    }
    # privateKey = web3.eth.account.decrypt(json.loads(encrypted_private_key), password)
    txn = func.buildTransaction(transaction)
    signed = web3.eth.account.signTransaction(txn, encrypted_private_key)
    txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

    # Wait for transaction to be mined
    receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    print(receipt)

    event = contract.events.ProjectCreated().processReceipt(receipt)
    return event[0]['args']
