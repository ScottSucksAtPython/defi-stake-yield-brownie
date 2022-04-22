# ------------------------------ Documentation ------------------------------ #
# Module:  deploy.py
# will deploy the TokenFarm and DappToken contracts.
#
#
# Modification History
# 04-20-2022 SRK Project Created.

# -------------------------------- Tasks ----------------------------------- #

# ------------------------------- Resources -------------------------------- #
from audioop import add
from tokenize import Token
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    deploy_mocks,
    fund_with_link,
)
from brownie import config, network, DappToken, TokenFarm
from web3 import Web3

# ------------------------------- Variables -------------------------------- #
KEPT_BALANCE = Web3.toWei(100, "ether")

# ------------------------------ Functions --------------------------------- #
def deploy_token_farm_and_dapp_token():
    """This function deploys the TokenFarm and DappToken contracts to the blockchain. It then transfers the entire supply of Dapp Tokens"""
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedToken(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm


# ----------------------------- Main Function ------------------------------ #
def main():
    deploy_token_farm_and_dapp_token()
