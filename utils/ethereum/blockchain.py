from datetime import datetime

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

    def get_auction(self,contract_address):
        return AuctionProvider(self.web3,contract_address,self.auction_abi)


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

    def fund(self, project_creator, pk):
        nonce = self.web3.eth.getTransactionCount(project_creator)
        gas_estimate = self.contract_instance.functions.fundProject().estimateGas({'from': project_creator})
        tx_hash = self.contract_instance.functions.fundProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': project_creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result
    def cancel(self, project_creator, pk):
        nonce = self.web3.eth.getTransactionCount(project_creator)
        gas_estimate = self.contract_instance.functions.cancelProject().estimateGas({'from': project_creator})
        tx_hash = self.contract_instance.functions.cancelProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': project_creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result
    def release(self, project_creator, pk):
        nonce = self.web3.eth.getTransactionCount(project_creator)
        gas_estimate = self.contract_instance.functions.releaseProject().estimateGas({'from': project_creator})
        tx_hash = self.contract_instance.functions.releaseProject().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': project_creator,
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

    def create_auction(self, a_creator, a_creator_pk, sale_token_num, min_val_per_token, bidding_time, delayed_start_time=0):
        nonce = self.web3.eth.getTransactionCount(a_creator)
        gas_estimate = self.contract_instance.functions.createAuction(sale_token_num, min_val_per_token, bidding_time,
                                                                      delayed_start_time).estimateGas(
            {'from': a_creator})
        tx_hash = self.contract_instance.functions.createAuction(sale_token_num, min_val_per_token, bidding_time,
                                                                      delayed_start_time).buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': a_creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=a_creator_pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result


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


class AuctionProvider:
    def __init__(self, web3, contract_address, abi):
        self.web3 = web3
        address = web3.toChecksumAddress(contract_address)
        self.contract_instance = web3.eth.contract(address=address, abi=abi)

    def cancel(self, auction_creator, pk):
        nonce = self.web3.eth.getTransactionCount(auction_creator)
        gas_estimate = self.contract_instance.functions.cancel().estimateGas({'from': auction_creator})
        tx_hash = self.contract_instance.functions.cancel().buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': auction_creator,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result

    def bid(self,bidder,pk,req_token_num,total_val):
        nonce = self.web3.eth.getTransactionCount(bidder)
        gas_estimate = self.contract_instance.functions.bid(req_token_num).estimateGas({'from': bidder,'value':total_val})
        tx_hash = self.contract_instance.functions.bid(req_token_num).buildTransaction({
            'gas': gas_estimate,
            'gasPrice': self.web3.eth.gasPrice,
            'from': bidder,
            'value':total_val,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=pk)
        sent_tx = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = self.web3.eth.wait_for_transaction_receipt(sent_tx)
        return result

if __name__ == '__main__':
    ss_adrs = '0x93798bD0950b697fE0E252eEaB07635c87371dCd'
    creator = '0x9d112fE3fA0740f789e6a49bf9Eb0e3563908438'
    manager = '0x881bEC6e019C959A4207501a1131f27bA25fc232'
    manager_pk = '0x7e8cd4add61c6e9b907492b1d02149a74b9dca7693a9711f84ce28a7b87f79b5'
    eth_p = ETHProvider(ss_adrs, manager, manager_pk)
    # print(eth_p.get_sharif_starter().get_total_supply())
    # print(eth_p.get_sharif_starter().balance_of(creator))

    # print("transfer func test:")
    # print(eth_p.get_sharif_starter().transfer('0x1917c9DAb2A42077701c72B9A2C855f4Fe10E041',
    #                                           '0x403c224223505bb9ee1e7817f905e78f1e7c15b2fd6c6af0b95bfc8e8493ca8a',
    #                                           '0xBD4a090365b7968053d3bCed09Cb5415941b95b1', 10 ** 19))

    p_creator = '0xd5861813d45aa520d5d560da02cd966582870234'
    p_creator_pk = '0xad35d3084a4871f03a638e192fea6849098bbfbebf1f57b49fc31b5ef5b195c9'

    # print("create project")
    # result =(eth_p.get_sharif_starter().create_project(p_creator,p_creator_pk
    #                                            ,eth_p.manager,
    #                                                 'jolback','JOLB','description',10000))
    #
    # project_address = result['logs'][0]['address']
    # print("project adrs: ",project_address)

    # project_address = '0xD332a42E13580EaD8b88f96176CDB6c24379EbB0'
    # p = eth_p.get_project(project_address)
    # print(p.get_details())
    # #
    # print(p.fund(p_creator, p_creator_pk))
    # print(p.approve_by_manager(manager,manager_pk))
    # print(p.release(p_creator, p_creator_pk))
    #
    # Create Auction
    # print("create auction")
    # bidding_time = int(60*5)
    # sale_token_num=100
    # min_val_per_token=10**17
    # result=p.create_auction(p_creator,p_creator_pk,sale_token_num,min_val_per_token,bidding_time)
    # print(result)

    auction_address ='0x7642521c320331561d65a20Da9B38BDc6ceaC517'
    a=eth_p.get_auction(auction_address).bid(p_creator,p_creator_pk,10,10000000000000000000)
    print(a)

# git hub token : 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
