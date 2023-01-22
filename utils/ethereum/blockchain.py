from web3 import Web3

ganache_url = 'http://127.0.0.1:8545'


class ETHProvider:
    def __init__(self, ss_address, manager, manager_pass):
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.ss_contract_address = ss_address
        self.manager = manager
        self.manager_pass = manager_pass
        try:
            self.ss_abi = open('../contract/SharifStarter.abi').read()
            self.project_abi = open('../contract/Project.abi').read()
            self.auction_abi = open('../contract/Auction.abi').read()
        except:
            print("ETHProvider failed to load sharif starter abi.")

    def get_sharif_starter(self):
        return SharifStarterProvider(self.web3, self.ss_contract_address, self.ss_abi)

    def create_eth_account(self, password):
        account = self.web3.eth.account.create()
        return account.address, account.encrypt(password)

    def get_balance(self, address):
        balance = self.web3.eth.getBalance(address)
        return self.web3.fromWei(balance, 'ether')

    def is_connected(self):
        return self.web3.isConnected()

    def get_project(self, contract_address):
        return ProjectProvider(self.web3, contract_address, self.project_abi)


class SharifStarterProvider:
    def __init__(self, web3, contract_address, abi):
        self.web3 = web3
        address = web3.toChecksumAddress(contract_address)
        self.contract_instance = web3.eth.contract(address=address, abi=abi)

    def get_symbol(self):
        symbol = self.contract_instance.functions.symbol().call()
        return symbol

    def get_total_supply(self):
        total = self.contract_instance.functions.totalSupply().call()
        return total

    def balance_of(self, account_address):
        return self.contract_instance.functions.balanceOf(account_address).call()

    def create_project(self, creator, pk, manager, name, symbol, description, total_supply):
        nonce = self.web3.eth.getTransactionCount(creator)
        gas_estimate = self.contract_instance.functions.createProject(manager, name, symbol, description,
                                                                      total_supply).estimateGas({'from': creator})
        tx_hash = self.contract_instance.functions.createProject(manager, name, symbol, description,
                                                                 total_supply).buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result

    def transfer(self, sender, private_key, to, amount):
        nonce = self.web3.eth.getTransactionCount(sender)
        gas_estimate = self.contract_instance.functions.transfer(to, amount).estimateGas({'from': sender})

        if gas_estimate < 100000:
            tx_hash = self.contract_instance.functions.transfer(to, amount).buildTransaction({
                'gas': gas_estimate,
                'gasPrice': self.web3.eth.gasPrice,
                'from': sender,
                'nonce': nonce,
            })

            signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=private_key)
            sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
            return result
        else:
            print("Gas cost exceeds 100000")
            return None


class ProjectProvider:
    def __init__(self, web3, contract_address, abi):
        self.web3 = web3
        address = web3.toChecksumAddress(contract_address)
        self.contract_instance = web3.eth.contract(address=address, abi=abi)

    def get_symbol(self):
        symbol = self.contract_instance.functions.symbol().call()
        return symbol

    def get_total_supply(self):
        total = self.contract_instance.functions.totalSupply().call()
        return total

    def get_manager(self):
        manager = self.contract_instance.functions.manager().call()
        return manager

    def get_stage(self):
        stage = self.contract_instance.functions.stage().call()
        return stage

    def is_approved_for_cf(self):
        is_approved = self.contract_instance.functions.isApprovedForCrowdFund().call()
        return is_approved

    def get_details(self):
        details = self.contract_instance.functions.projectDetails().call()
        return details

    def fund(self,creator,pk):
        nonce = self.web3.eth.getTransactionCount(creator)
        gas_estimate = self.contract_instance.functions.fundProject().estimateGas({'from': creator})
        tx_hash = self.contract_instance.functions.fundProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result
    def release(self,creator,pk):
        nonce = self.web3.eth.getTransactionCount(creator)
        gas_estimate = self.contract_instance.functions.releaseProject().estimateGas({'from': creator})
        tx_hash = self.contract_instance.functions.releaseProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result

    def approve_by_manager(self, manager, manager_pk):
        nonce = self.web3.eth.getTransactionCount(manager)
        gas_estimate = self.contract_instance.functions.approveProject().estimateGas({'from': manager})
        tx_hash = self.contract_instance.functions.approveProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': manager,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=manager_pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result

    def create_auction(self,):
        pass

    def set_shareholders(self, sender, private_key, shareholders, amount):
        # TODO
        results = []
        for to in shareholders:
            nonce = self.web3.eth.getTransactionCount(sender)
            gas_estimate = self.contract_instance.functions.transfer(to, amount).estimateGas({'from': sender})

            if gas_estimate < 100000:
                tx_hash = self.contract_instance.functions.transfer(to, amount).buildTransaction({
                    'gas': gas_estimate,
                    'gasPrice': self.web3.eth.gasPrice,
                    'from': sender,
                    'nonce': nonce,
                })

                signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=private_key)
                sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
            return result
        else:
            print("Gas cost exceeds 100000")
            return None


if __name__ == '__main__':
    eth_p = ETHProvider('0x44e5f3d39aDBdb0950d88F24128016947Ef634D4', '0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041',
                        '')
    print(eth_p.get_sharif_starter().get_total_supply())
    print(eth_p.get_sharif_starter().balance_of('0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041'))

    # print("transfer func test:")
    # print(eth_p.get_sharif_starter().transfer('0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041',
    #                                           '0x403c224223505bb9ee1e7817f905e78f1e7c15b2fd6c6af0b95bfc8e8493ca8a',
    #                                           '0xBD4a090365b7968053d3bCed09Cb5415941b95b1', 10 ** 19))

    # print("create project")
    # print(eth_p.get_sharif_starter().create_project('0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041',
    #                                            '0x403c224223505bb9ee1e7817f905e78f1e7c15b2fd6c6af0b95bfc8e8493ca8a',eth_p.manager,
    #                                                 'tousradieh','Tous','',10000))

    project_address = '0x216Ebb9F3bB39B7437122FE77BcFe974836872E0'
    creator = '0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041'
    creator_pass = '0x403c224223505bb9ee1e7817f905e78f1e7c15b2fd6c6af0b95bfc8e8493ca8a'
    print(eth_p.get_project(project_address).get_details())
