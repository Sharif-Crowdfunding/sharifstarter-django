from wallet.models import TokenAsset


def mint_token(project):
    balance = (project.token_info.total_supply * 8) / 10
    t = TokenAsset(wallet=project.user.wallet, contract_address=project.contract_address,
                   symbol=project.token_info.symbol, balance=balance)
    t.save()

def update_token_for_user(project,wallet):
    token_asset = TokenAsset.objects.get(wallet=wallet,contract_address=project.contract_address)
    balance = token_asset.balance
    token_asset.update_balance()

def transfer_token():
    pass
